from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.constructor_arguments import ConstructorArguments
    from ..models.contract_source import ContractSource
    from ..models.external_library import ExternalLibrary
    from ..models.smart_contract_compiler_settings import SmartContractCompilerSettings


T = TypeVar("T", bound="SmartContract")


@_attrs_define
class SmartContract:
    """
    Attributes:
        verified_twin_address_hash (Union[Unset, str]):  Example: 0x394c399dbA25B99Ab7708EdB505d755B3aa29997.
        is_verified (Union[Unset, bool]):
        is_changed_bytecode (Union[Unset, bool]):
        is_partially_verified (Union[Unset, bool]):
        is_fully_verified (Union[Unset, bool]):
        is_verified_via_sourcify (Union[Unset, bool]):
        is_verified_via_eth_bytecode_db (Union[Unset, bool]):
        is_vyper_contract (Union[Unset, bool]):
        is_self_destructed (Union[Unset, bool]):
        can_be_visualized_via_sol2uml (Union[Unset, bool]):
        minimal_proxy_address_hash (Union[Unset, str]):  Example: 0x394c399dbA25B99Ab7708EdB505d755B3aa29997.
        sourcify_repo_url (Union[Unset, str]):  Example: https://sourcify.repo.com/100/link_to_a_contract_at_sourcify.
        name (Union[Unset, str]):  Example: Cryptostamp3L2.
        optimization_enabled (Union[Unset, bool]):
        optimizations_runs (Union[Unset, int]):  Example: 200.
        compiler_version (Union[Unset, str]):  Example: v0.8.4+commit.c7e474f2.
        evm_version (Union[Unset, str]):  Example: default.
        verified_at (Union[Unset, str]):  Example: 2021-06-02T17:54:17.116055Z.
        abi (Union[Unset, str]):  Example: [{"type":"constructor","stateMutability":"nonpayable","inputs":[{"type":"addr
            ess","name":"_bridgeDataAddress","internalType":"address"},{"type":"uint256","name":"_finalSupply","internalType
            ":"uint256"},{"type":"uint256[5]","name":"_totalColorSupply","internalType":"uint256[5]"}]}].
        source_code (Union[Unset, str]):  Example: contract A {}.
        file_path (Union[Unset, str]):  Example: contract.sol.
        compiler_settings (Union[Unset, SmartContractCompilerSettings]):  Example: {'compilationTarget':
            {'@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol': 'ERC1967Proxy'}, 'evmVersion': 'london', 'libraries':
            {}, 'metadata': {'bytecodeHash': 'ipfs'}, 'optimizer': {'enabled': True, 'runs': 200}, 'remappings': []}.
        constructor_args (Union[Unset, str]):  Example: 0x01.
        additional_sources (Union[Unset, list['ContractSource']]):
        decoded_constructor_args (Union[Unset, list['ConstructorArguments']]):
        deployed_bytecode (Union[Unset, str]):  Example: 0x01.
        creation_bytecode (Union[Unset, str]):  Example: 0x02.
        external_libraries (Union[Unset, list['ExternalLibrary']]):
        language (Union[Unset, str]):  Example: solidity | vyper | yul.
    """

    verified_twin_address_hash: Union[Unset, str] = UNSET
    is_verified: Union[Unset, bool] = UNSET
    is_changed_bytecode: Union[Unset, bool] = UNSET
    is_partially_verified: Union[Unset, bool] = UNSET
    is_fully_verified: Union[Unset, bool] = UNSET
    is_verified_via_sourcify: Union[Unset, bool] = UNSET
    is_verified_via_eth_bytecode_db: Union[Unset, bool] = UNSET
    is_vyper_contract: Union[Unset, bool] = UNSET
    is_self_destructed: Union[Unset, bool] = UNSET
    can_be_visualized_via_sol2uml: Union[Unset, bool] = UNSET
    minimal_proxy_address_hash: Union[Unset, str] = UNSET
    sourcify_repo_url: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    optimization_enabled: Union[Unset, bool] = UNSET
    optimizations_runs: Union[Unset, int] = UNSET
    compiler_version: Union[Unset, str] = UNSET
    evm_version: Union[Unset, str] = UNSET
    verified_at: Union[Unset, str] = UNSET
    abi: Union[Unset, str] = UNSET
    source_code: Union[Unset, str] = UNSET
    file_path: Union[Unset, str] = UNSET
    compiler_settings: Union[Unset, "SmartContractCompilerSettings"] = UNSET
    constructor_args: Union[Unset, str] = UNSET
    additional_sources: Union[Unset, list["ContractSource"]] = UNSET
    decoded_constructor_args: Union[Unset, list["ConstructorArguments"]] = UNSET
    deployed_bytecode: Union[Unset, str] = UNSET
    creation_bytecode: Union[Unset, str] = UNSET
    external_libraries: Union[Unset, list["ExternalLibrary"]] = UNSET
    language: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        verified_twin_address_hash = self.verified_twin_address_hash

        is_verified = self.is_verified

        is_changed_bytecode = self.is_changed_bytecode

        is_partially_verified = self.is_partially_verified

        is_fully_verified = self.is_fully_verified

        is_verified_via_sourcify = self.is_verified_via_sourcify

        is_verified_via_eth_bytecode_db = self.is_verified_via_eth_bytecode_db

        is_vyper_contract = self.is_vyper_contract

        is_self_destructed = self.is_self_destructed

        can_be_visualized_via_sol2uml = self.can_be_visualized_via_sol2uml

        minimal_proxy_address_hash = self.minimal_proxy_address_hash

        sourcify_repo_url = self.sourcify_repo_url

        name = self.name

        optimization_enabled = self.optimization_enabled

        optimizations_runs = self.optimizations_runs

        compiler_version = self.compiler_version

        evm_version = self.evm_version

        verified_at = self.verified_at

        abi = self.abi

        source_code = self.source_code

        file_path = self.file_path

        compiler_settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.compiler_settings, Unset):
            compiler_settings = self.compiler_settings.to_dict()

        constructor_args = self.constructor_args

        additional_sources: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.additional_sources, Unset):
            additional_sources = []
            for additional_sources_item_data in self.additional_sources:
                additional_sources_item = additional_sources_item_data.to_dict()
                additional_sources.append(additional_sources_item)

        decoded_constructor_args: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.decoded_constructor_args, Unset):
            decoded_constructor_args = []
            for decoded_constructor_args_item_data in self.decoded_constructor_args:
                decoded_constructor_args_item = decoded_constructor_args_item_data.to_dict()
                decoded_constructor_args.append(decoded_constructor_args_item)

        deployed_bytecode = self.deployed_bytecode

        creation_bytecode = self.creation_bytecode

        external_libraries: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.external_libraries, Unset):
            external_libraries = []
            for external_libraries_item_data in self.external_libraries:
                external_libraries_item = external_libraries_item_data.to_dict()
                external_libraries.append(external_libraries_item)

        language = self.language

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if verified_twin_address_hash is not UNSET:
            field_dict["verified_twin_address_hash"] = verified_twin_address_hash
        if is_verified is not UNSET:
            field_dict["is_verified"] = is_verified
        if is_changed_bytecode is not UNSET:
            field_dict["is_changed_bytecode"] = is_changed_bytecode
        if is_partially_verified is not UNSET:
            field_dict["is_partially_verified"] = is_partially_verified
        if is_fully_verified is not UNSET:
            field_dict["is_fully_verified"] = is_fully_verified
        if is_verified_via_sourcify is not UNSET:
            field_dict["is_verified_via_sourcify"] = is_verified_via_sourcify
        if is_verified_via_eth_bytecode_db is not UNSET:
            field_dict["is_verified_via_eth_bytecode_db"] = is_verified_via_eth_bytecode_db
        if is_vyper_contract is not UNSET:
            field_dict["is_vyper_contract"] = is_vyper_contract
        if is_self_destructed is not UNSET:
            field_dict["is_self_destructed"] = is_self_destructed
        if can_be_visualized_via_sol2uml is not UNSET:
            field_dict["can_be_visualized_via_sol2uml"] = can_be_visualized_via_sol2uml
        if minimal_proxy_address_hash is not UNSET:
            field_dict["minimal_proxy_address_hash"] = minimal_proxy_address_hash
        if sourcify_repo_url is not UNSET:
            field_dict["sourcify_repo_url"] = sourcify_repo_url
        if name is not UNSET:
            field_dict["name"] = name
        if optimization_enabled is not UNSET:
            field_dict["optimization_enabled"] = optimization_enabled
        if optimizations_runs is not UNSET:
            field_dict["optimizations_runs"] = optimizations_runs
        if compiler_version is not UNSET:
            field_dict["compiler_version"] = compiler_version
        if evm_version is not UNSET:
            field_dict["evm_version"] = evm_version
        if verified_at is not UNSET:
            field_dict["verified_at"] = verified_at
        if abi is not UNSET:
            field_dict["abi"] = abi
        if source_code is not UNSET:
            field_dict["source_code"] = source_code
        if file_path is not UNSET:
            field_dict["file_path"] = file_path
        if compiler_settings is not UNSET:
            field_dict["compiler_settings"] = compiler_settings
        if constructor_args is not UNSET:
            field_dict["constructor_args"] = constructor_args
        if additional_sources is not UNSET:
            field_dict["additional_sources"] = additional_sources
        if decoded_constructor_args is not UNSET:
            field_dict["decoded_constructor_args"] = decoded_constructor_args
        if deployed_bytecode is not UNSET:
            field_dict["deployed_bytecode"] = deployed_bytecode
        if creation_bytecode is not UNSET:
            field_dict["creation_bytecode"] = creation_bytecode
        if external_libraries is not UNSET:
            field_dict["external_libraries"] = external_libraries
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.constructor_arguments import ConstructorArguments
        from ..models.contract_source import ContractSource
        from ..models.external_library import ExternalLibrary
        from ..models.smart_contract_compiler_settings import SmartContractCompilerSettings

        d = dict(src_dict)
        verified_twin_address_hash = d.pop("verified_twin_address_hash", UNSET)

        is_verified = d.pop("is_verified", UNSET)

        is_changed_bytecode = d.pop("is_changed_bytecode", UNSET)

        is_partially_verified = d.pop("is_partially_verified", UNSET)

        is_fully_verified = d.pop("is_fully_verified", UNSET)

        is_verified_via_sourcify = d.pop("is_verified_via_sourcify", UNSET)

        is_verified_via_eth_bytecode_db = d.pop("is_verified_via_eth_bytecode_db", UNSET)

        is_vyper_contract = d.pop("is_vyper_contract", UNSET)

        is_self_destructed = d.pop("is_self_destructed", UNSET)

        can_be_visualized_via_sol2uml = d.pop("can_be_visualized_via_sol2uml", UNSET)

        minimal_proxy_address_hash = d.pop("minimal_proxy_address_hash", UNSET)

        sourcify_repo_url = d.pop("sourcify_repo_url", UNSET)

        name = d.pop("name", UNSET)

        optimization_enabled = d.pop("optimization_enabled", UNSET)

        optimizations_runs = d.pop("optimizations_runs", UNSET)

        compiler_version = d.pop("compiler_version", UNSET)

        evm_version = d.pop("evm_version", UNSET)

        verified_at = d.pop("verified_at", UNSET)

        abi = d.pop("abi", UNSET)

        source_code = d.pop("source_code", UNSET)

        file_path = d.pop("file_path", UNSET)

        _compiler_settings = d.pop("compiler_settings", UNSET)
        compiler_settings: Union[Unset, SmartContractCompilerSettings]
        if isinstance(_compiler_settings, Unset):
            compiler_settings = UNSET
        else:
            compiler_settings = SmartContractCompilerSettings.from_dict(_compiler_settings)

        constructor_args = d.pop("constructor_args", UNSET)

        additional_sources = []
        _additional_sources = d.pop("additional_sources", UNSET)
        for additional_sources_item_data in _additional_sources or []:
            additional_sources_item = ContractSource.from_dict(additional_sources_item_data)

            additional_sources.append(additional_sources_item)

        decoded_constructor_args = []
        _decoded_constructor_args = d.pop("decoded_constructor_args", UNSET)
        for decoded_constructor_args_item_data in _decoded_constructor_args or []:
            decoded_constructor_args_item = ConstructorArguments.from_dict(decoded_constructor_args_item_data)

            decoded_constructor_args.append(decoded_constructor_args_item)

        deployed_bytecode = d.pop("deployed_bytecode", UNSET)

        creation_bytecode = d.pop("creation_bytecode", UNSET)

        external_libraries = []
        _external_libraries = d.pop("external_libraries", UNSET)
        for external_libraries_item_data in _external_libraries or []:
            external_libraries_item = ExternalLibrary.from_dict(external_libraries_item_data)

            external_libraries.append(external_libraries_item)

        language = d.pop("language", UNSET)

        smart_contract = cls(
            verified_twin_address_hash=verified_twin_address_hash,
            is_verified=is_verified,
            is_changed_bytecode=is_changed_bytecode,
            is_partially_verified=is_partially_verified,
            is_fully_verified=is_fully_verified,
            is_verified_via_sourcify=is_verified_via_sourcify,
            is_verified_via_eth_bytecode_db=is_verified_via_eth_bytecode_db,
            is_vyper_contract=is_vyper_contract,
            is_self_destructed=is_self_destructed,
            can_be_visualized_via_sol2uml=can_be_visualized_via_sol2uml,
            minimal_proxy_address_hash=minimal_proxy_address_hash,
            sourcify_repo_url=sourcify_repo_url,
            name=name,
            optimization_enabled=optimization_enabled,
            optimizations_runs=optimizations_runs,
            compiler_version=compiler_version,
            evm_version=evm_version,
            verified_at=verified_at,
            abi=abi,
            source_code=source_code,
            file_path=file_path,
            compiler_settings=compiler_settings,
            constructor_args=constructor_args,
            additional_sources=additional_sources,
            decoded_constructor_args=decoded_constructor_args,
            deployed_bytecode=deployed_bytecode,
            creation_bytecode=creation_bytecode,
            external_libraries=external_libraries,
            language=language,
        )

        smart_contract.additional_properties = d
        return smart_contract

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
