#!/usr/bin/env python2.7
# coding=utf-8
'''
WTForms Extend Field
copy form https://github.com/rduplain/flask-wtf/

Copyright (c) 2010 by Dan Jacob.

Some rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above
  copyright notice, this list of conditions and the following
  disclaimer in the documentation and/or other materials provided
  with the distribution.

* The names of the contributors may not be used to endorse or
  promote products derived from this software without specific
  prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

from wtforms import TextField
from wtforms import IntegerField as _IntegerField
from wtforms import DecimalField as _DecimalField
from wtforms import DateField as _DateField
from wtforms.widgets import Input

class DateInput(Input):
    """
    Creates `<input type=date>` widget
    """
    input_type = "date"


class NumberInput(Input):
    """
    Creates `<input type=number>` widget
    """
    input_type="number"


class RangeInput(Input):
    """
    Creates `<input type=range>` widget
    """
    input_type="range"


class URLInput(Input):
    """
    Creates `<input type=url>` widget
    """
    input_type = "url"


class EmailInput(Input):
    """
    Creates `<input type=email>` widget
    """

    input_type = "email"


class SearchInput(Input):
    """
    Creates `<input type=search>` widget
    """

    input_type = "search"

class TelInput(Input):
    """
    Creates `<input type=tel>` widget
    """

    input_type = "tel"


class SearchField(TextField):
    """
    **TextField** using **SearchInput** by default
    """
    widget = SearchInput()


class DateField(_DateField):
    """
    **DateField** using **DateInput** by default
    """
 
    widget = DateInput()


class URLField(TextField):
    """
    **TextField** using **URLInput** by default
    """
 
    widget = URLInput()
    

class EmailField(TextField):
    """
    **TextField** using **EmailInput** by default
    """
 
    widget = EmailInput()

class TelField(TextField):
    """
    **TextField** using **TelInput** by default
    """

    widget = TelInput()


class IntegerField(_IntegerField):
    """
    **IntegerField** using **NumberInput** by default
    """

    widget = NumberInput()


class DecimalField(_DecimalField):
    """
    **DecimalField** using **NumberInput** by default
    """

    widget = NumberInput()


class IntegerRangeField(_IntegerField):
    """
    **IntegerField** using **RangeInput** by default
    """

    widget = RangeInput()


class DecimalRangeField(_DecimalField):
    """
    **DecimalField** using **RangeInput** by default
    """

    widget = RangeInput()
