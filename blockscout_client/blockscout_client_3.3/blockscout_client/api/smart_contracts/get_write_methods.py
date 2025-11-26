from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.write_method import WriteMethod
from ...types import UNSET, Response, Unset


def _get_kwargs(
    address_hash: str,
    *,
    is_custom_abi: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["is_custom_abi"] = is_custom_abi

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/v2/smart-contracts/{address_hash}/methods-write",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, list["WriteMethod"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = WriteMethod.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[Any, list["WriteMethod"]]]:
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
    is_custom_abi: Union[Unset, str] = UNSET,
) -> Response[Union[Any, list["WriteMethod"]]]:
    """get verified smart-contract write methods

    Args:
        address_hash (str):
        is_custom_abi (Union[Unset, str]):  Example: true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, list['WriteMethod']]]
    """

    kwargs = _get_kwargs(
        address_hash=address_hash,
        is_custom_abi=is_custom_abi,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    address_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
    is_custom_abi: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, list["WriteMethod"]]]:
    """get verified smart-contract write methods

    Args:
        address_hash (str):
        is_custom_abi (Union[Unset, str]):  Example: true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, list['WriteMethod']]
    """

    return sync_detailed(
        address_hash=address_hash,
        client=client,
        is_custom_abi=is_custom_abi,
    ).parsed


async def asyncio_detailed(
    address_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
    is_custom_abi: Union[Unset, str] = UNSET,
) -> Response[Union[Any, list["WriteMethod"]]]:
    """get verified smart-contract write methods

    Args:
        address_hash (str):
        is_custom_abi (Union[Unset, str]):  Example: true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, list['WriteMethod']]]
    """

    kwargs = _get_kwargs(
        address_hash=address_hash,
        is_custom_abi=is_custom_abi,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    address_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
    is_custom_abi: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, list["WriteMethod"]]]:
    """get verified smart-contract write methods

    Args:
        address_hash (str):
        is_custom_abi (Union[Unset, str]):  Example: true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, list['WriteMethod']]
    """

    return (
        await asyncio_detailed(
            address_hash=address_hash,
            client=client,
            is_custom_abi=is_custom_abi,
        )
    ).parsed
