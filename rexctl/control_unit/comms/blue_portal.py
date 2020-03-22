import bluetooth
import yaml

from ...util.singleton import Singleton


class BluePortal(metaclass=Singleton):

    def __init__(self):
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", bluetooth.PORT_ANY))
        self.server_sock.listen(1)
        self.port = self.server_sock.getsockname()[1]
        self.uuid = "3b6bdzew-4876-01qa-h47f-2e739ce21125"

    async def start(self):
        while True:
            bluetooth.advertise_service(self.server_sock, "rex-portal", service_id=self.uuid,
                                        service_classes=[self.uuid, bluetooth.SERIAL_PORT_CLASS],
                                        profiles=[bluetooth.SERIAL_PORT_PROFILE],
                                        # protocols=[bluetooth.OBEX_UUID]
                                        )
            # TODO implement logging
            # print("Waiting for connection on RFCOMM channel", self.port)
            client_sock, client_info = self.server_sock.accept()
            # print("Accepted connection from", client_info)
            try:
                while True:
                    data = client_sock.recv(1024)
                    if not data:
                        break
                    # print("Received", data)
                    from control_unit.rex_daemon import RexDaemon
                    RexDaemon().exec(yaml.load(data))
            except OSError:
                # TODO handle errors
                pass
            # print("Disconnected.")
            client_sock.close()

    def stop(self):
        self.server_sock.close()
