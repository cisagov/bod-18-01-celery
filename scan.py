#!/usr/bin/env python3

"""scan is a tool to...

Usage:
  scan (INPUT ...) [--debug]
  scan (-h | --help)

Options:
  -h --help                     Show this message.
  -d --debug                    Print debug output.
"""

import docopt

import bod1801.__version__
from bod1801.tasks import sslyze, trustymail


def main():
    args = docopt.docopt(__doc__, version=bod1801.__version__)  # noqa: F841

    domain_names = [
        'dhs.gov',
        'nasa.gov'
    ]
    smtp_ports = [
        25,
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

    for domain_name in domain_names:
        trustymail_result = trustymail.delay(domain_name=domain_name,
                                             smtp_ports=smtp_ports,
                                             scan_types=scan_types,
                                             dns_hostnames=dns_hostnames)
        trustymail_answer = trustymail_result.get()
        print('Trustymail result for {} is: {}'.format(domain_name,
                                                       trustymail_answer))

        starttls = trustymail_answer['Domain Supports STARTTLS Results']
        servers_and_ports = [
            s.strip()
            for s in starttls.split(',')
        ]

        for server_and_port in servers_and_ports:
            temp = server_and_port.split(':')
            server = temp[0]
            port = temp[1]

            starttls_smtp = True
            scan_tlsv10 = True
            scan_tlsv11 = False
            scan_tlsv12 = False
            scan_tlsv13 = False
            scan_sslv20 = False
            scan_sslv30 = False
            scan_cert_info = False

            sslyze_result = sslyze.delay(hostname=server,
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
            print('\tSslyze result for {} is: {}'.format(server_and_port,
                                                         sslyze_answer))


if __name__ == '__main__':
    main()
