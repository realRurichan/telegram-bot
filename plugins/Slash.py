import re
import requests
from functools import partial
from loguru import logger as _logger
from typing import Optional, Union, Any, Callable
from telegram import Update, Message
from telegram.ext import MessageHandler, filters, CallbackContext

'''
Codes from https://github.com/Rongronggg9/SlashBot
'''


def load():
    _logger.info("SlashPlugin is loaded.")

Filters = filters

parser = re.compile(
    r'^(?P<slash>[\\/]_?\$?)'
    r'(?P<predicate>([^\s\\]|\\.)*((?<=\S)\\)?)'
    r'(\s+(?P<complement>.+))?$'
)


convertEscapes = partial(re.compile(r'\\(\s)').sub, r'\1')
htmlEscape = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
mentionParser = re.compile(r'@([a-zA-Z]\w{4,})')

PUNCTUATION_TAIL = '.,?!;:~(' \
                   '。，？！；：～（'

def log(func: Callable):
    def wrapper(update: Update, ctx: CallbackContext):
        logger = ctx.bot_data['logger']
        logger.debug(str(update.to_dict()))
        return func(update, ctx, logger)

    return wrapper


class User:
    def __init__(self, uid: Optional[int] = None, username: Optional[str] = None, name: Optional[str] = None):
        if not (uid and name) and not username:
            raise ValueError('invalid user')
        self.name = name
        self.uid = uid
        self.username = username
        if not self.name and self.username:
            self.__get_user_by_username()

    def __get_user_by_username(self):
        r = requests.get(f'https://t.me/{self.username}')
        self.name = re.search(r'(?<=<meta property="og:title" content=").*(?=")', r.text, re.IGNORECASE).group(0)
        page_title = re.search(r'(?<=<title>).*(?=</title>)', r.text, re.IGNORECASE).group(0)
        if page_title == self.name:  # user does not exist
            self.name = None

    def mention(self, mention_self: bool = False, pure: bool = False) -> str:
        if not self.name:
            return f'@{self.username}'

        mention_deep_link = (f'tg://resolve?domain={self.username}'
                             if (self.username and (not self.uid or self.uid < 0))
                             else f'tg://user?id={self.uid}')
        name = self.name if not mention_self else "自己"
        return f'<a href="{mention_deep_link}">{name}</a>' if not pure else name

    def __eq__(self, other):
        return (
                type(self) == type(other)
                and (
                        ((self.uid or other.uid) and self.uid == other.uid) or
                        ((self.username or other.username) and self.username == other.username)
                )
        )

def get_user(msg: Message) -> User:
    user = msg.sender_chat or msg.from_user
    return User(name=user.full_name or user.title, uid=user.id, username=user.username)

def get_users(msg: Message) -> tuple[User, User]:
    msg_from = msg
    msg_rpl = msg.reply_to_message or msg_from
    from_user, rpl_user = get_user(msg_from), get_user(msg_rpl)
    return from_user, rpl_user

async def parse_command(ctx: CallbackContext) -> Optional[dict[str, Union[str, bool]]]:
    username = await ctx.bot.get_me()
    username = username.username
    print(username)
    match = ctx.match
    parsed = match.groupdict()
    predicate = parsed['predicate']
    complement = parsed['complement']
    if not predicate and complement:
        return None  # invalid command

    omit_le = predicate.endswith('\\')
    predicate = predicate[:-1] if omit_le else predicate
    predicate = convertEscapes(predicate)
    predicate = partial(re.compile(username, re.I).sub,'')(predicate)
    result = {'predicate': htmlEscape(predicate),
              'complement': htmlEscape(complement or ''),
              'slash': parsed['slash'],
              'swap': parsed['slash'] not in ('/', '/$'),
              'omit_le': omit_le}
    return result

def get_tail(tail_char: str) -> str:
    if tail_char in PUNCTUATION_TAIL:
        return ''
    halfwidth_mark = tail_char.isascii()
    return '!' if halfwidth_mark else '！'

def get_text(user_from: User, user_rpl: User, command: dict):
    rpl_self = user_from == user_rpl
    mention_from = user_from.mention()
    mention_rpl = user_rpl.mention(mention_self=rpl_self)
    slash, predicate, complement, omit_le = \
        command['slash'], command['predicate'], command['complement'], command['omit_le']

    if predicate == '':
        ret = '!' if not command['swap'] else '¡'
    elif predicate == 'me':
        ret = f"{mention_from}{bool(complement) * ' '}{complement}"
        ret += get_tail((complement or user_from.mention(pure=True))[-1])
    elif predicate == 'you':
        ret = f"{mention_rpl}{bool(complement) * ' '}{complement}"
        ret += get_tail((complement or user_rpl.mention(mention_self=rpl_self, pure=True))[-1])
    elif complement:
        ret = f"{mention_from} {predicate} {mention_rpl} {complement}"
        ret += get_tail(complement[-1])
    else:
        ret = f"{mention_from} {predicate} "
        ret += '了 ' if not omit_le else ''
        ret += mention_rpl
        ret += get_tail(mention_rpl[-1])
    return ret

async def reply(update: Update, ctx: CallbackContext):
    username = await ctx.bot.get_me()
    username = username.username
    command = await parse_command(ctx)
    if not command:
        return
    logger = _logger.bind(username=username)
    logger.debug(str(update.to_dict()))
    msg = update.effective_message
    from_user, rpl_user = get_users(msg)

    if from_user == rpl_user:
        mention_match = mentionParser.search(command['predicate'])
        if mention_match:
            mention = mentionParser.search(msg.text).group(1)
            rpl_user = User(username=mention)
            command['predicate'] = command['predicate'][:mention_match.start()]
        else:
            mention_match = mentionParser.search(command['complement'])
            if mention_match:
                mention = mentionParser.search(msg.text).group(1)
                rpl_user = User(username=mention)
                complement = command['complement']
                complement = complement[:mention_match.start()] + complement[mention_match.end():]
                command['complement'] = complement.strip()

    if command['swap'] and (not from_user == rpl_user):
        (from_user, rpl_user) = (rpl_user, from_user)

    text = get_text(from_user, rpl_user, command)
    logger.info("Slash replied: " + text)

    await update.effective_message.reply_text('\u200e' + text, parse_mode='HTML')

handlers = [MessageHandler(Filters.Regex(parser) & ~Filters.UpdateType.EDITED & ~filters.COMMAND, reply)]
