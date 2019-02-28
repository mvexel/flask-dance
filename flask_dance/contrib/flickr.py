from __future__ import unicode_literals

from flask_dance.consumer import OAuth1ConsumerBlueprint
from functools import partial
from flask.globals import LocalProxy, _lookup_app_object

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


__maintainer__ = "Martijn van Exel <m@rtijn.org>"


def make_flickr_blueprint(
    api_key=None,
    api_secret=None,
    redirect_url=None,
    redirect_to=None,
    login_url=None,
    authorized_url=None,
    session_class=None,
    backend=None,
    storage=None,
):
    """
    Make a blueprint for authenticating with Flickr using OAuth 1. This requires
    an API key and API secret from Flickr. You should either pass them to
    this constructor, or make sure that your Flask application config defines
    them, using the variables FLICKR_OAUTH_API_KEY and FLICKR_OAUTH_API_SECRET.

    Args:
        api_key (str): The API key for your Flickr application
        api_secret (str): The API secret for your Flickr application
        redirect_url (str): the URL to redirect to after the authentication
            dance is complete
        redirect_to (str): if ``redirect_url`` is not defined, the name of the
            view to redirect to after the authentication dance is complete.
            The actual URL will be determined by :func:`flask.url_for`
        login_url (str, optional): the URL path for the ``login`` view.
            Defaults to ``/flickr``
        authorized_url (str, optional): the URL path for the ``authorized`` view.
            Defaults to ``/flickr/authorized``.
        session_class (class, optional): The class to use for creating a
            Requests session. Defaults to
            :class:`~flask_dance.consumer.requests.OAuth1Session`.
        storage: A token storage class, or an instance of a token storage
                class, to use for this blueprint. Defaults to
                :class:`~flask_dance.consumer.storage.session.SessionStorage`.

    :rtype: :class:`~flask_dance.consumer.OAuth1ConsumerBlueprint`
    :returns: A :ref:`blueprint <flask:blueprints>` to attach to your Flask app.
    """
    flickr_bp = OAuth1ConsumerBlueprint(
        "flickr",
        __name__,
        client_key=api_key,
        client_secret=api_secret,
        base_url="https://api.flickr.com/services/rest/?method=",
        request_token_url="https://www.flickr.com/services/oauth/request_token",
        access_token_url="https://www.flickr.com/services/oauth/access_token",
        authorization_url="https://www.flickr.com/services/oauth/authorize",
        redirect_url=redirect_url,
        redirect_to=redirect_to,
        login_url=login_url,
        authorized_url=authorized_url,
        session_class=session_class,
        backend=backend,
        storage=storage,
    )
    flickr_bp.from_config["client_key"] = "FLICKR_OAUTH_API_KEY"
    flickr_bp.from_config["client_secret"] = "FLICKR_OAUTH_API_SECRET"

    @flickr_bp.before_app_request
    def set_applocal_session():
        ctx = stack.top
        ctx.flickr_oauth = flickr_bp.session

    return flickr_bp


flickr = LocalProxy(partial(_lookup_app_object, "flickr_oauth"))
