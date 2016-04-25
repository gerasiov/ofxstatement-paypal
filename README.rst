.. image:: https://travis-ci.org/themalkolm/ofxstatement-paypal.svg?branch=master
    :target: https://travis-ci.org/themalkolm/ofxstatement-paypal

This is a collection of parsers for proprietary statement formats, produced by
`PayPal`_. It parses ``*.csv`` file exported from the site.

It is a plugin for `ofxstatement`_.

.. _PayPal: https://www.paypal.com
.. _ofxstatement: https://github.com/kedder/ofxstatement

Example
=======

.. code-block::

    [paypal_sek]
    plugin = paypal
    locale = sv_SE
    account_id = john.doe@gmail.com
    currency = SEK
    analyze = 1

    [paypal_eur]
    plugin = paypal
    locale = sv_SE
    account_id = john.doe@gmail.com
    currency = EUR
    analyze = 1