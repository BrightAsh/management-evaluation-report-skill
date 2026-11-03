#!/usr/bin/env python3
"""content.json의 내용을 ○로 가린 사본을 만든다. 공개용 예시 지면(PDF·이미지)을 만들 때 쓴다.

가리는 것: 제목, 본문, 숫자, 기관명, 열 머리, 흐름 시기 태그, 머리말·바닥글 문구 등 모든 내용 글자
          그림은 지우고 같은 크기의 회색 자리표시로 바꾼다
남기는 것: 블록 모양, 칸 이름(현황 및 문제점·추진내용·추진성과 등), 번호, B.P 태그, 기호(→ ➡ · % 등), 쪽 번호

사용법: python3 tools/mask_content.py content.json content_masked.json
"""
import json, re, sys

KEEP_KEYS = {'t', 'no', 'align', 'on', 'w', 'w_mm', 'h_mm', 'kw_mm', 'pos', 'sep', 'c', 'header'}
KEEP_LABEL_KEYS = {'k', 'label'}          # 칸 이름: grid·kv·line의 k, ev·key·res의 label
LETTER = re.compile(r'[0-9A-Za-z가-힣ㄱ-ㆎ一-鿿]')


def mask(s):
    return LETTER.sub('○', s)


def mask_footer(s):
    m = re.match(r'^(.*?)(\d+)\s*$', s)          # 끝의 쪽 번호는 남긴다
    if m and '│' in s and s.strip().endswith(m.group(2)):
        return mask(m.group(1)) + m.group(2)
    head = re.match(r'^(\d+)(\s*│.*)$', s)        # 앞의 쪽 번호
    if head:
        return head.group(1) + mask(head.group(2))
    return mask(s)


def walk(node, key=None, parent_t=None):
    if isinstance(node, dict):
        t = node.get('t', parent_t)
        out = {}
        for k, v in node.items():
            if k == 'src':                           # 그림은 지우고 자리표시로
                out[k] = None
            elif k == 'tag':                         # B.P처럼 구조 태그는 남기고, 흐름 시기 등 내용 태그는 가린다
                out[k] = v if t in ('sec', 'sub') and re.fullmatch(r'[A-Za-z.\s①-⑩]+', str(v)) else mask(str(v))
            elif k == 't' and isinstance(v, list):    # 흐름도 단계 설명(t: [...])은 내용이므로 가린다
                out[k] = walk(v, k, t)
            elif k in KEEP_KEYS or isinstance(v, bool):
                out[k] = v
            elif k in KEEP_LABEL_KEYS and isinstance(v, (str, list)):
                out[k] = v
            elif k == 'footer':
                out[k] = mask_footer(v)
            elif k == 'title' and key is None:
                out[k] = v + ' (마스킹)'
            elif k == 'config':
                out[k] = mask_config(v)
            else:
                out[k] = walk(v, k, t)
        return out
    if isinstance(node, list):
        return [walk(x, key, parent_t) for x in node]
    if isinstance(node, str):
        return mask(node)
    return node


def mask_config(cfg):
    cfg = json.loads(json.dumps(cfg))
    lay = cfg.get('layout')
    if lay:
        for k in ('running', 'org', 'slogan', 'sidetab'):
            if lay.get(k):
                lay[k] = mask(lay[k])
        if lay.get('chapter', {}).get('text'):
            lay['chapter']['text'] = mask(lay['chapter']['text'])
    return cfg


def main():
    src, dst = sys.argv[1], sys.argv[2]
    data = json.load(open(src, encoding='utf-8'))
    json.dump(walk(data), open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('ok:', dst)


if __name__ == '__main__':
    main()
