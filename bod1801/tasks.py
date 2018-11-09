import json

from boto3 import client as boto3_client

from .celery import app

# The name of the AWS region to use
AwsRegionName = 'us-west-1'

# The name of the trustymail Lambda function
TrustymailLambdaName = 'trustymail'

# The name of the sslyze Lambda function
SslyzeLambdaName = 'sslyze'


@app.task
def trustymail(domain_name, timeout=30, smtp_timeout=5,
               smtp_localhost=None, smtp_ports=None,
               scan_types=None, dns_hostnames=None):
    """Perform a trustymail scan.

    Parameters
    ----------
    domain_name : str
        A string containing the domain to be scanned.  For example,
        "dhs.gov".
    timeout : int
        An integer denoting the DNS lookup timeout in seconds.
    smtp_timeout : int
        An integer denoting the SMTP connection timeout in seconds.
    smtp_localhost : str
        A string containing the host name to use when connecting to
        SMTP servers.  If None then the fully-qualified domain name of
        the Lambda host is used.
    smtp_ports : list
        A list of integers, each of which is a port on which to look
        for SMTP servers.  If None then the default list containing
        25, 465, and 587 is used.
    scan_types : dict
        A dictionary consisting of the required keys "mx", "starttls",
        "spf", and "dmarc".  The corresponding values are booleans
        indicating whether or not the scan type is to be performed.
        If None then all scan types are performed.
    dns_hostnames : list
        A list of strings, each corresponding to a DNS server.  For
        example, to use Google DNS use the value "['8.8.8.8',
        '8.8.4.4']".  If None then the DNS configuration of the Lambda
        host ("/etc/resolv.conf") is used.

    Returns
    -------
    dict
        A dict specifying the fields of the trustymail.domain.Domain
        object resulting from the scan activity.
    """
    # Boto3 client for Lambda
    lambda_client = boto3_client('lambda', region_name=AwsRegionName)

    # The payload for the Lambda function
    payload = {
        'domain_name': domain_name,
        'timeout': timeout,
        'smtp_timeout': smtp_timeout,
        'smtp_localhost': smtp_localhost,
        'smtp_ports': smtp_ports,
        'scan_types': scan_types,
        'dns_hostnames': dns_hostnames
    }

    # Perform a synchronous Lambda call
    response = lambda_client.invoke(FunctionName=TrustymailLambdaName,
                                    InvocationType='RequestResponse',
                                    LogType='None',
                                    Payload=json.dumps(payload))

    return json.loads(response['Payload'].read())


@app.task
def sslyze(hostname, port=443, timeout=5, starttls_smtp=False,
           scan_tlsv10=False, scan_tlsv11=False,
           scan_tlsv12=False, scan_tlsv13=False,
           scan_sslv20=False, scan_sslv30=False,
           scan_cert_info=False):
    """Perform an sslyze scan.

    Parameters
    ----------
    hostname : str
        A string containing the hostname to be scanned.  For example,
        "dhs.gov".
    port : int
        An integer specifying the port to be scanned.  If omitted then
        the default value of 443 is used.
    timeout : int
        An integer denoting the number of seconds to wait when
        creating a connection.  If omitted then the default value of 5
        is used.
    starttls_smtp : bool
        A boolean value denoting whether to try to use STARTTLS after
        connecting to an SMTP server.  This option should be True is
        connecting to an SMTP host and otherwise False.  If omitted
        then the default value of False is used.
    scan_tlsv10 : bool
        A boolean value denoting whether to scan for TLS version 1.0
        ciphers. If omitted then the default value of False is used.
    scan_tlsv11 : bool
        A boolean value denoting whether to scan for TLS version 1.1
        ciphers. If omitted then the default value of False is used.
    scan_tlsv12 : bool
        A boolean value denoting whether to scan for TLS version 1.2
        ciphers. If omitted then the default value of False is used.
    scan_tlsv13 : bool
        A boolean value denoting whether to scan for TLS version 1.3
        ciphers. If omitted then the default value of False is used.
    scan_sslv20 : bool
        A boolean value denoting whether to scan for SSL version 2.0
        ciphers. If omitted then the default value of False is used.
    scan_sslv30 : bool
        A boolean value denoting whether to scan for SSL version 3.0
        ciphers. If omitted then the default value of False is used.
    scan_cert_info : bool
        A boolean value denoting whether to return certificate
        information.  If omitted then the default value of False is
        used.

    Returns
    -------
    OrderedDict
        An OrderedDict specifying the fields of the
        trustymail.domain.Domain object resulting from the scan
        activity.
    """
    # Boto3 client for Lambda
    lambda_client = boto3_client('lambda', region_name=AwsRegionName)

    # The payload for the Lambda function
    payload = {
        'hostname': hostname,
        'port': port,
        'timeout': timeout,
        'starttls_smtp': starttls_smtp,
        'scan_tlsv10': scan_tlsv10,
        'scan_tlsv11': scan_tlsv11,
        'scan_tlsv12': scan_tlsv12,
        'scan_tlsv13': scan_tlsv13,
        'scan_sslv20': scan_sslv20,
        'scan_sslv30': scan_sslv30,
        'scan_cert_info': scan_cert_info
    }

    # Perform a synchronous Lambda call
    response = lambda_client.invoke(FunctionName=SslyzeLambdaName,
                                    InvocationType='RequestResponse',
                                    LogType='None',
                                    Payload=json.dumps(payload))

    return json.loads(response['Payload'].read())
