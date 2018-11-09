#!/usr/bin/env python3

"""scan is a tool to...

Usage:
  scan (INPUT ...) [--debug]
  scan (-h | --help)

Options:
  -h --help                     Show this message.
  -d --debug                    Print debug output.
"""

import logging

import docopt

import bod1801.tasks


def main():
    args = docopt.docopt(__doc__, version=bod1801.__version__)

    domain_name = 'dhs.gov'
    smtp_ports = [
        25
    ]
    scan_types = {
        'mx': True,
        'starttls': True,
        'spf': True,
        'dmarc': True
    }
    dns_hostnames = [
        '8.8.8.8',
        '8.8.4.4'
    ]
    trustymail_result = bod1801.tasks.trustymail.delay(domain_name=domain_name,
                                                       smtp_ports=smtp_ports,
                                                       scan_types=scan_types,
                                                       dns_hostnames=dns_hostnames)
    trustymail_answer = trustymail_result.get()
    print('Trustymail result is: {}'.format(trustymail_answer))

    hostname = trustymail_answer['Mail Servers']
    port = int(trustymail_answer['Mail Server Ports Tested'])
    starttls_smtp = True
    scan_tlsv10 = True
    scan_tlsv11 = False
    scan_tlsv12 = False
    scan_tlsv13 = False
    scan_sslv20 = False
    scan_sslv30 = False
    scan_cert_info = False

    sslyze_result = bod1801.tasks.sslyze.delay(hostname=hostname,
                                               port=port,
                                               starttls_smtp=starttls_smtp,
                                               scan_tlsv10=scan_tlsv10,
                                               scan_tlsv11=scan_tlsv11,
                                               scan_tlsv12=scan_tlsv12,
                                               scan_tlsv13=scan_tlsv13,
                                               scan_sslv20=scan_sslv20,
                                               scan_sslv30=scan_sslv30,
                                               scan_cert_info=scan_cert_info)
    sslyze_answer = sslyze_result.get()
    print('Sslyze result is: {}'.format(sslyze_answer))


if __name__ == '__main__':
    main()
