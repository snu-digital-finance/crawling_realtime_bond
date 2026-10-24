import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

import requests

URL = "https://www.kofiabond.or.kr/proframeWeb/XMLSERVICES/"
TIMEOUT_SECONDS = 60


def _body(service: str, function: str, slots: dict[int, str]) -> str:
    vals = "".join(f"\n    <val{i}>{escape(v)}</val{i}>" for i, v in slots.items())
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n<message>\n  <proframeHeader>\n'
        f"    <pfmAppName>BIS-KOFIABOND</pfmAppName>\n    <pfmSvcName>{service}</pfmSvcName>\n"
        f"    <pfmFnName>{function}</pfmFnName>\n  </proframeHeader>\n  <systemHeader></systemHeader>\n"
        f"    <BISComDspDatDTO>{vals}\n</BISComDspDatDTO>\n</message>"
    )


def fetch_rows(
    service: str,
    function: str,
    wmonid: str,
    vals: dict[int, str],
    extra_slots: tuple[int, ...] = (),
) -> list[dict[str, str]]:
    slots = dict.fromkeys((*range(1, 8), *extra_slots), "")
    slots.update(vals)
    response = requests.post(
        URL,
        headers={"Content-Type": "application/xml", "Cookie": f"WMONID={wmonid}"},
        data=_body(service, function, slots).encode("utf-8"),
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    root = ET.fromstring(response.text)
    if int(root.find(".//dbio_total_count_").text) == 0:
        return []
    return [
        {child.tag: child.text or "" for child in dto}
        for dto in root.findall(".//BISComDspDatDTO")
    ]
