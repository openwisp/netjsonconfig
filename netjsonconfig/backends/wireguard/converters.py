from ..base.converter import BaseConverter
from .schema import schema

wireguard_definitions = schema["properties"]["wireguard"]["items"]
peer_definitions = wireguard_definitions["properties"]["peers"]["items"]


class Wireguard(BaseConverter):
    netjson_key = "wireguard"
    intermediate_key = "wireguard"
    _schema = schema
    _forward_property_map = {
        "port": "ListenPort",
        "private_key": "PrivateKey",
        "address": "Address",
        "dns": "DNS",
        "mtu": "MTU",
        "save_config": "SaveConfig",
        "table": "Table",
        "pre_up": "PreUp",
        "post_up": "PostUp",
        "pre_down": "PreDown",
        "post_down": "PostDown",
    }

    def to_intermediate_loop(self, block, result, index=None):
        vpn = self.__intermediate_vpn(block)
        result.setdefault("wireguard", [])
        result["wireguard"].append(vpn)
        return result

    def __intermediate_vpn(self, config, remove=None):
        # Required properties
        for option in ["port", "private_key", "address"]:
            config[self._forward_property_map[option]] = config.pop(option)
        # Optional properties
        for option in self._forward_property_map.keys():
            if option in ["port", "private_key", "address"]:
                # These options have been already handled
                continue
            if config.get(option, None) not in ["", None, []]:
                if option == "dns":
                    config[option] = ",".join(config[option])
                elif option == "save_config":
                    config[option] = "true" if config[option] else "false"
                config[self._forward_property_map[option]] = config.pop(option)
            else:
                config.pop(option, None)
        config["peers"] = self.__intermediate_peers(config.get("peers", []))
        return self.sorted_dict(config)

    def to_netjson_loop(self, block, result, index):
        vpn = self.__netjson_vpn(block)
        result.setdefault("wireguard", [])
        result["wireguard"].append(vpn)
        return result

    def __netjson_vpn(self, vpn):
        backward_property_map = {
            value: key for key, value in self._forward_property_map.items()
        }
        peers = vpn.pop("peers", [])
        for native, netjson in backward_property_map.items():
            if native not in vpn:
                continue
            value = vpn.pop(native)
            if netjson == "dns":
                value = [item.strip() for item in value.split(",") if item.strip()]
            elif netjson == "save_config" and not isinstance(value, bool):
                value = str(value).lower() == "true"
            vpn[netjson] = value
        vpn = self.type_cast(vpn, wireguard_definitions)
        vpn["peers"] = self.__netjson_peers(peers)
        if not vpn["peers"]:
            del vpn["peers"]
        return vpn

    def __netjson_peers(self, peers):
        peer_list = []
        for peer in peers:
            peer = dict(peer)
            if "AllowedIPs" in peer:
                peer["allowed_ips"] = peer.pop("AllowedIPs")
            if "PublicKey" in peer:
                peer["public_key"] = peer.pop("PublicKey")
            if "PreSharedKey" in peer:
                peer["preshared_key"] = peer.pop("PreSharedKey")
            endpoint = peer.pop("Endpoint", None)
            if endpoint:
                # the port is separated by the last colon, so that
                # IPv6 endpoints are not split on their own colons
                host, separator, port = endpoint.rpartition(":")
                if separator:
                    peer["endpoint_host"] = host
                    peer["endpoint_port"] = port
                else:
                    peer["endpoint_host"] = endpoint
            peer_list.append(self.sorted_dict(self.type_cast(peer, peer_definitions)))
        return peer_list

    def __intermediate_peers(self, peers):
        peer_list = []
        for peer in peers:
            peer["AllowedIPs"] = peer.pop("allowed_ips")
            peer["PublicKey"] = peer.pop("public_key")
            peer["PreSharedKey"] = peer.pop("preshared_key", None)
            host = peer.pop("endpoint_host", None)
            port = peer.pop("endpoint_port", None)
            if host and port:
                peer["Endpoint"] = f"{host}:{port}"
            peer_list.append(self.sorted_dict(peer))
        return peer_list
