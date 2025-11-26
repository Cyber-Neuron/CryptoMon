from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_block_txs_response_200 import GetBlockTxsResponse200
from ...types import Response


def _get_kwargs(
    block_number_or_hash: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/v2/blocks/{block_number_or_hash}/transactions",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetBlockTxsResponse200]]:
    if response.status_code == 200:
        response_200 = GetBlockTxsResponse200.from_dict(response.json())

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
) -> Response[Union[Any, GetBlockTxsResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    block_number_or_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, GetBlockTxsResponse200]]:
    """get block transactions

    Args:
        block_number_or_hash (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetBlockTxsResponse200]]
    """

    kwargs = _get_kwargs(
        block_number_or_hash=block_number_or_hash,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    block_number_or_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, GetBlockTxsResponse200]]:
    """get block transactions

    Args:
        block_number_or_hash (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetBlockTxsResponse200]
    """

    return sync_detailed(
        block_number_or_hash=block_number_or_hash,
        client=client,
    ).parsed


async def asyncio_detailed(
    block_number_or_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, GetBlockTxsResponse200]]:
    """get block transactions

    Args:
        block_number_or_hash (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetBlockTxsResponse200]]
    """

    kwargs = _get_kwargs(
        block_number_or_hash=block_number_or_hash,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    block_number_or_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, GetBlockTxsResponse200]]:
    """get block transactions

    Args:
        block_number_or_hash (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetBlockTxsResponse200]
    """

    return (
        await asyncio_detailed(
            block_number_or_hash=block_number_or_hash,
            client=client,
        )
    ).parsed
