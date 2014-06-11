#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sublime, sublime_plugin
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
  maskWithoutBlank = re.compile("`[a-zA-Z0-9/=\-+*%<>!&|\^.~@]+`")
  mask = re.compile(" *`[a-zA-Z0-9/=\-+*%<>!&|\^.~]+@` *")

  mtexts = []
  for m in re.finditer(maskWithoutBlank, string):
    mtexts.append(m.group())

  mtexts = tuple(mtexts)

  string = mask.sub('%s', string.replace('%', '%%'))

  print 'string', string
  print 'mtexts', mtexts

  # replace
  aDict = {
    r' *\, *':'，',
    r' *\. *':'。',
    r' *\! *':'！',
    r' *\? *':'？',
    r' *\: *':'：',
    r' *\[ *':'【',
    r' *\] *':'】',
    r' *\( *':'（',
    r' *\) *':'）',
    r' *\{ *':'｛',
    r' *\} *':'｝'
    }
  return multi_replace(aDict, string) % mtexts

class ChignCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    regions = self.view.sel()

    print regions
    for region in regions:
      string = self.view.substr(region)
      self.view.replace(edit, region, process(string))
