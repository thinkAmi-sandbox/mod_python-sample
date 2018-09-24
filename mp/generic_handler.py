# /usr/bin/python
# -*- codeing: utf-8 -*-
from mod_python import apache, util, Cookie, psp


def handler(req):
    req.content_type = 'text/plain'
    req.headers_out['X-My-header'] = 'hello world'

    cookies = Cookie.get_cookies(req)
    if 'counter' in cookies:
        c = cookies['counter']
        c.value = int(c.value) + 1
        Cookie.add_cookie(req, c)
    else:
        Cookie.add_cookie(req, 'counter', '1')

    # get query string / POST data
    # see: https://stackoverflow.com/a/27448720
    fields = util.FieldStorage(req)

    # NOTE: use req.write() after set HTTP headers
    if 'note' in fields:
        # NG
        req.write('set after body\n')
        Cookie.add_cookie(req, 'after_write', 'yes')
        req.headers_out['X-After-Write'] = 'oh'
        return apache.OK

        # OK
        # Cookie.add_cookie(req, 'after_write', 'yes')
        # req.headers_out['X-After-Write'] = 'oh'
        # req.write('set after body\n')
        # return apache.OK

    # Usage PSP template
    if fields.get('psp', None):
        req.content_type = 'text/html'
        template = psp.PSP(req, filename='template.html')
        template.run({'query_string': fields.get('psp', None)})
        return apache.OK

    if '404' in fields:
        return apache.HTTP_NOT_FOUND

    if 'error' in fields:
        return apache.SERVER_RETURN

    if 'redirect' in fields:
        util.redirect(req, 'https://www.google.co.jp')

    # OK - get CGI environment value
    if 'env1' in fields:
        req.add_common_vars()
        env = req.subprocess_env
        # get CGI value: HTTP_HOST
        host = env.get('HTTP_HOST')
        req.write('subprocess_env(HTTP_HOST): {}\n'.format(host))

    # NG - get CGI environment value
    if 'env2' in fields:
        env = req.subprocess_env
        host = env.get('HTTP_HOST')
        req.write('subprocess_env(HTTP_HOST): {}\n'.format(host))
        return apache.OK
            
    # NG - get CGI environment value
    # NEED mod_python 3.4.1 over
    if 'env3' in fields:
        req.add_cgi_vars()
        env = req.subprocess_env
        req.write(env.get('HTTP_HOST', 'foo'))
        return apache.OK

    # Write Request object
    req.write('request.args: {}\n'.format(req.args))
    # => None / foo=bar

    req.write('request.method: {}\n'.format(req.method))
    # => GET

    # Why: return apache.OK / req.status
    req.write('request.status: {}\n'.format(req.status))
    # => 200

    req.write('request.filename: {}\n'.format(req.filename))
    # => /var/www/mpytest/mp/generic_handler.py

    req.write('request.get_remote_host(): {}\n'.format(
        req.get_remote_host(apache.REMOTE_NOLOOKUP)
    ))
    # => 192.168.69.1

    # request HTTP header
    # headers_in is dict like object (mod_python.apache.table)
    for k, v in req.headers_in.items():
        req.write('headers_in:  key -> {} / value -> {}\n'.format(k, v))

    for k, v in fields.items():
        req.write('FieldStorage:  key -> {} / value -> {}\n'.format(k, v))

    req.write('Hello world')

    # output HTTP Status Code
    return apache.OK
