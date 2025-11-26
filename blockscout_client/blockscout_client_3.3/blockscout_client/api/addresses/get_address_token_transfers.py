from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_address_token_transfers_response_200 import GetAddressTokenTransfersResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    address_hash: str,
    *,
    type_: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    token: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["type"] = type_

    params["filter"] = filter_

    params["token"] = token

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/v2/addresses/{address_hash}/token-transfers",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetAddressTokenTransfersResponse200]]:
    if response.status_code == 200:
        response_200 = GetAddressTokenTransfersResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, GetAddressTokenTransfersResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    address_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
    type_: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    token: Union[Unset, str] = UNSET,
) -> Response[Union[Any, GetAddressTokenTransfersResponse200]]:
    """get address token transfers

    Args:
        address_hash (str):
        type_ (Union[Unset, str]):  Example: ERC-20,ERC-721,ERC-1155.
        filter_ (Union[Unset, str]):  Example: to | from.
        token (Union[Unset, str]):  Example: 0xb81afe27c103bcd42f4026cf719af6d802928765.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetAddressTokenTransfersResponse200]]
    """

    kwargs = _get_kwargs(
        address_hash=address_hash,
        type_=type_,
        filter_=filter_,
        token=token,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    address_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
    type_: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    token: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, GetAddressTokenTransfersResponse200]]:
    """get address token transfers

    Args:
        address_hash (str):
        type_ (Union[Unset, str]):  Example: ERC-20,ERC-721,ERC-1155.
        filter_ (Union[Unset, str]):  Example: to | from.
        token (Union[Unset, str]):  Example: 0xb81afe27c103bcd42f4026cf719af6d802928765.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetAddressTokenTransfersResponse200]
    """

    return sync_detailed(
        address_hash=address_hash,
        client=client,
        type_=type_,
        filter_=filter_,
        token=token,
    ).parsed


async def asyncio_detailed(
    address_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
    type_: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    token: Union[Unset, str] = UNSET,
) -> Response[Union[Any, GetAddressTokenTransfersResponse200]]:
    """get address token transfers

    Args:
        address_hash (str):
        type_ (Union[Unset, str]):  Example: ERC-20,ERC-721,ERC-1155.
        filter_ (Union[Unset, str]):  Example: to | from.
        token (Union[Unset, str]):  Example: 0xb81afe27c103bcd42f4026cf719af6d802928765.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetAddressTokenTransfersResponse200]]
    """

    kwargs = _get_kwargs(
        address_hash=address_hash,
        type_=type_,
        filter_=filter_,
        token=token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    address_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
    type_: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    token: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, GetAddressTokenTransfersResponse200]]:
    """get address token transfers

    Args:
        address_hash (str):
        type_ (Union[Unset, str]):  Example: ERC-20,ERC-721,ERC-1155.
        filter_ (Union[Unset, str]):  Example: to | from.
        token (Union[Unset, str]):  Example: 0xb81afe27c103bcd42f4026cf719af6d802928765.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetAddressTokenTransfersResponse200]
    """

    return (
        await asyncio_detailed(
            address_hash=address_hash,
            client=client,
            type_=type_,
            filter_=filter_,
            token=token,
        )
    ).parsed
