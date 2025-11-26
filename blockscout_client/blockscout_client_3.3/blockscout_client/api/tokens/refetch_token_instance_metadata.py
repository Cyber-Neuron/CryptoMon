from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.recaptcha_body import RecaptchaBody
from ...models.refetch_token_instance_metadata_response_200 import RefetchTokenInstanceMetadataResponse200
from ...models.refetch_token_instance_metadata_response_403 import RefetchTokenInstanceMetadataResponse403
from ...types import Response


def _get_kwargs(
    address_hash: str,
    id: int,
    *,
    body: RecaptchaBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/api/v2/tokens/{address_hash}/instances/{id}/refetch-metadata",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[RefetchTokenInstanceMetadataResponse200, RefetchTokenInstanceMetadataResponse403]]:
    if response.status_code == 200:
        response_200 = RefetchTokenInstanceMetadataResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 403:
        response_403 = RefetchTokenInstanceMetadataResponse403.from_dict(response.json())

        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[RefetchTokenInstanceMetadataResponse200, RefetchTokenInstanceMetadataResponse403]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    address_hash: str,
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: RecaptchaBody,
) -> Response[Union[RefetchTokenInstanceMetadataResponse200, RefetchTokenInstanceMetadataResponse403]]:
    """re-fetch token instance metadata

    Args:
        address_hash (str):
        id (int):
        body (RecaptchaBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RefetchTokenInstanceMetadataResponse200, RefetchTokenInstanceMetadataResponse403]]
    """

    kwargs = _get_kwargs(
        address_hash=address_hash,
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    address_hash: str,
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: RecaptchaBody,
) -> Optional[Union[RefetchTokenInstanceMetadataResponse200, RefetchTokenInstanceMetadataResponse403]]:
    """re-fetch token instance metadata

    Args:
        address_hash (str):
        id (int):
        body (RecaptchaBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RefetchTokenInstanceMetadataResponse200, RefetchTokenInstanceMetadataResponse403]
    """

    return sync_detailed(
        address_hash=address_hash,
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    address_hash: str,
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: RecaptchaBody,
) -> Response[Union[RefetchTokenInstanceMetadataResponse200, RefetchTokenInstanceMetadataResponse403]]:
    """re-fetch token instance metadata

    Args:
        address_hash (str):
        id (int):
        body (RecaptchaBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RefetchTokenInstanceMetadataResponse200, RefetchTokenInstanceMetadataResponse403]]
    """

    kwargs = _get_kwargs(
        address_hash=address_hash,
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    address_hash: str,
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: RecaptchaBody,
) -> Optional[Union[RefetchTokenInstanceMetadataResponse200, RefetchTokenInstanceMetadataResponse403]]:
    """re-fetch token instance metadata

    Args:
        address_hash (str):
        id (int):
        body (RecaptchaBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RefetchTokenInstanceMetadataResponse200, RefetchTokenInstanceMetadataResponse403]
    """

    return (
        await asyncio_detailed(
            address_hash=address_hash,
            id=id,
            client=client,
            body=body,
        )
    ).parsed
