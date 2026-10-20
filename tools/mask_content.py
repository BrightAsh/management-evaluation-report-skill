#!/usr/bin/env python3
"""content.json의 내용을 ○로 가린 사본을 만든다. 공개용 예시 지면(PDF·이미지)을 만들 때 쓴다.

가리는 것: 제목, 본문, 숫자, 기관명 등 모든 내용 글자(한글·영문·숫자)
남기는 것: 블록 모양, 칸 이름(문제점·추진내용·추진성과 등), 번호, B.P 태그, 기호(→ ➡ · % 등), 쪽 번호

사용법: python3 tools/mask_content.py content.json content_masked.json
"""
import json, re, sys

KEEP_KEYS = {'t', 'no', 'tag', 'align', 'on', 'w', 'w_mm', 'h_mm', 'src', 'config'}
KEEP_LABEL_KEYS = {'k', 'label'}          # 칸 이름: kv·line·eff의 k, ev·res·bp의 label
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


def walk(node, key=None):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k == 't' and isinstance(v, list):    # 흐름도 단계 설명(t: [...])은 내용이므로 가린다
                out[k] = walk(v, k)
            elif k in KEEP_KEYS:
                out[k] = v
            elif k in KEEP_LABEL_KEYS and isinstance(v, (str, list)):
                out[k] = v
            elif k == 'footer':
                out[k] = mask_footer(v)
            elif k == 'title' and key is None:
                out[k] = v + ' (마스킹)'
            else:
                out[k] = walk(v, k)
        return out
    if isinstance(node, list):
        return [walk(x, key) for x in node]
    if isinstance(node, str):
        return mask(node)
    return node


def main():
    src, dst = sys.argv[1], sys.argv[2]
    data = json.load(open(src, encoding='utf-8'))
    masked = walk(data)
    for page in masked.get('pages', []):        # 블록 안의 'tag'는 남기되 sub 태그(내용성)는 가린다
        for b in page['blocks']:
            if b.get('t') == 'sub' and 'tag' in b:
                b['tag'] = mask(b['tag'])
    json.dump(masked, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('ok:', dst)


if __name__ == '__main__':
    main()
