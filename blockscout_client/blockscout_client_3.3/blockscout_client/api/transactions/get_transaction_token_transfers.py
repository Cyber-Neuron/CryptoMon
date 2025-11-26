from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_transaction_token_transfers_response_200 import GetTransactionTokenTransfersResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    transaction_hash: str,
    *,
    type_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["type"] = type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/v2/transactions/{transaction_hash}/token-transfers",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetTransactionTokenTransfersResponse200]]:
    if response.status_code == 200:
        response_200 = GetTransactionTokenTransfersResponse200.from_dict(response.json())

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
) -> Response[Union[Any, GetTransactionTokenTransfersResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    transaction_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
    type_: Union[Unset, str] = UNSET,
) -> Response[Union[Any, GetTransactionTokenTransfersResponse200]]:
    """get transaction token transfers

    Args:
        transaction_hash (str):
        type_ (Union[Unset, str]):  Example: ERC-20,ERC-721,ERC-1155.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetTransactionTokenTransfersResponse200]]
    """

    kwargs = _get_kwargs(
        transaction_hash=transaction_hash,
        type_=type_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    transaction_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
    type_: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, GetTransactionTokenTransfersResponse200]]:
    """get transaction token transfers

    Args:
        transaction_hash (str):
        type_ (Union[Unset, str]):  Example: ERC-20,ERC-721,ERC-1155.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetTransactionTokenTransfersResponse200]
    """

    return sync_detailed(
        transaction_hash=transaction_hash,
        client=client,
        type_=type_,
    ).parsed


async def asyncio_detailed(
    transaction_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
    type_: Union[Unset, str] = UNSET,
) -> Response[Union[Any, GetTransactionTokenTransfersResponse200]]:
    """get transaction token transfers

    Args:
        transaction_hash (str):
        type_ (Union[Unset, str]):  Example: ERC-20,ERC-721,ERC-1155.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetTransactionTokenTransfersResponse200]]
    """

    kwargs = _get_kwargs(
        transaction_hash=transaction_hash,
        type_=type_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    transaction_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
    type_: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, GetTransactionTokenTransfersResponse200]]:
    """get transaction token transfers

    Args:
        transaction_hash (str):
        type_ (Union[Unset, str]):  Example: ERC-20,ERC-721,ERC-1155.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetTransactionTokenTransfersResponse200]
    """

    return (
        await asyncio_detailed(
            transaction_hash=transaction_hash,
            client=client,
            type_=type_,
        )
    ).parsed
