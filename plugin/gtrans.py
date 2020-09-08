#!/usr/bin/env python3
import vim
from googletrans import Translator

def __do_visual(buff, cur, res=''):
    cursor = cur.window.cursor

    if cursor[0] == buff.mark('<')[0]:

        if buff.mark('<')[0] == buff.mark('>')[0]:

            return buff[
                buff.mark('<')[0] - 1][
                    buff.mark('<')[1]:buff.mark('>')[1]]
        else:
            res = buff[buff.mark('<')[0] - 1][buff.mark('<')[1]:]

            for x in xrange(buff.mark('>')[0] - buff.mark('<')[0] - 1):
                res = ' '.join((res, buff[buff.mark('<')[0] + x]))

            return ' '.join((
                res,
                buff[buff.mark('>')[0] - 1][:buff.mark('>')[1]]))


def translate(content , to_lang):
    translator = Translator(service_urls=['translate.google.cn',])
    trans=translator.translate(content, src='auto', dest=to_lang)
    return '|' + trans.text + '|'

def vim_gtranslate():
    to_lang = vim.eval('g:gtrans_output_language') or 'zh-cn'

    buff = vim.current.buffer
    cur = vim.current
    cursor = cur.window.cursor
    res = ''
    if buff.mark('<') and buff.mark('>') and cursor[1] == 0 \
            and buff.mark('<')[0] <= cursor[0] <= buff.mark('>')[0]:
        # visual mode
        res = __do_visual(buff, cur)
    else:
        # cursor mode
        res = vim.eval('expand("<cword>")')

    translated = ''
    try:
        translated = translate(res if res else '' , to_lang)
    except Exception:
        pass
    vim.command (':call s:ShowTransWindow("%s")' % translated)
