#! /usr/bin/env python
# -*- coding: utf-8 -*-

# import sublime, sublime_plugin
from string import maketrans
import sys, re

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def multi_replace(aDict, subject):

  for k, kv in aDict.iteritems():
    r = re.compile(k)
    subject = r.sub(kv, subject)

  return subject

def process(string):

  # mask `something`
  maskWithoutBlank = re.compile("`[a-zA-Z0-9/=\-+*%<>!&|\^.~]+`")
  mask = re.compile(" *`[a-zA-Z0-9/=\-+*%<>!&|\^.~]+` *")

  mtexts = []
  for m in re.finditer(maskWithoutBlank, string):
    mtexts.append(m.group())

  mtexts = tuple(mtexts)

  string = string.replace('%', '%%')
  string = mask.sub('%s', string)

  print 'string', string
  print 'mtexts', mtexts

  # replace
  aDict = {
    r', *':'，',
    r'\. *':'。',
    r'\! *':'！',
    r'\? *':'？',
    r': *':'：',
    r' *\[':'[',
    r' *\]':']'
    }
  return multi_replace(aDict, string) % mtexts

# string = '这个运算符把两个向量的 `x` 相加, 把向量的 `y` 相减. 因为他实际是属于加减运算, 所以让它保持了和加法一样的结合性和优先级 (`left` 和 `140`).  查阅完整的Swift默认结合性和优先级的设置, 请移步 [表达式](Expressions)'
# 
string = "一个数除于0 `i / 0`, 或者对0求余数 `i % 0`, 就会产生一个错误."

# string = 'hello, world!`shit`'

print process(string)