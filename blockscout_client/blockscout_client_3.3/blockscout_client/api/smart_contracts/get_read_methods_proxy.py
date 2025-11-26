from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.read_method_with_value import ReadMethodWithValue
from ...models.read_method_without_value import ReadMethodWithoutValue
from ...types import UNSET, Response, Unset


def _get_kwargs(
    address_hash: str,
    *,
    is_custom_abi: Union[Unset, str] = UNSET,
    from_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["is_custom_abi"] = is_custom_abi

    params["from"] = from_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/v2/smart-contracts/{address_hash}/methods-read-proxy",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list[Union["ReadMethodWithValue", "ReadMethodWithoutValue"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:

            def _parse_response_200_item(data: object) -> Union["ReadMethodWithValue", "ReadMethodWithoutValue"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    response_200_item_type_0 = ReadMethodWithValue.from_dict(data)

                    return response_200_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_item_type_1 = ReadMethodWithoutValue.from_dict(data)

                return response_200_item_type_1

            response_200_item = _parse_response_200_item(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list[Union["ReadMethodWithValue", "ReadMethodWithoutValue"]]]:
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
    from_: Union[Unset, str] = UNSET,
) -> Response[list[Union["ReadMethodWithValue", "ReadMethodWithoutValue"]]]:
    """get verified smart-contract read methods proxy

    Args:
        address_hash (str):
        is_custom_abi (Union[Unset, str]):  Example: true.
        from_ (Union[Unset, str]):  Example: 0xF61f5c4a3664501F499A9289AaEe76a709CE536e.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[Union['ReadMethodWithValue', 'ReadMethodWithoutValue']]]
    """

    kwargs = _get_kwargs(
        address_hash=address_hash,
        is_custom_abi=is_custom_abi,
        from_=from_,
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
    from_: Union[Unset, str] = UNSET,
) -> Optional[list[Union["ReadMethodWithValue", "ReadMethodWithoutValue"]]]:
    """get verified smart-contract read methods proxy

    Args:
        address_hash (str):
        is_custom_abi (Union[Unset, str]):  Example: true.
        from_ (Union[Unset, str]):  Example: 0xF61f5c4a3664501F499A9289AaEe76a709CE536e.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[Union['ReadMethodWithValue', 'ReadMethodWithoutValue']]
    """

    return sync_detailed(
        address_hash=address_hash,
        client=client,
        is_custom_abi=is_custom_abi,
        from_=from_,
    ).parsed


async def asyncio_detailed(
    address_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
    is_custom_abi: Union[Unset, str] = UNSET,
    from_: Union[Unset, str] = UNSET,
) -> Response[list[Union["ReadMethodWithValue", "ReadMethodWithoutValue"]]]:
    """get verified smart-contract read methods proxy

    Args:
        address_hash (str):
        is_custom_abi (Union[Unset, str]):  Example: true.
        from_ (Union[Unset, str]):  Example: 0xF61f5c4a3664501F499A9289AaEe76a709CE536e.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[Union['ReadMethodWithValue', 'ReadMethodWithoutValue']]]
    """

    kwargs = _get_kwargs(
        address_hash=address_hash,
        is_custom_abi=is_custom_abi,
        from_=from_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    address_hash: str,
    *,
    client: Union[AuthenticatedClient, Client],
    is_custom_abi: Union[Unset, str] = UNSET,
    from_: Union[Unset, str] = UNSET,
) -> Optional[list[Union["ReadMethodWithValue", "ReadMethodWithoutValue"]]]:
    """get verified smart-contract read methods proxy

    Args:
        address_hash (str):
        is_custom_abi (Union[Unset, str]):  Example: true.
        from_ (Union[Unset, str]):  Example: 0xF61f5c4a3664501F499A9289AaEe76a709CE536e.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[Union['ReadMethodWithValue', 'ReadMethodWithoutValue']]
    """

    return (
        await asyncio_detailed(
            address_hash=address_hash,
            client=client,
            is_custom_abi=is_custom_abi,
            from_=from_,
        )
    ).parsed
