import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",  # Opera
]

headers_initial = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9,pl;q=0.8,ar;q=0.7",
    "cookie": "SOCS=CAISHAgCEhJnd3NfMjAyNDEwMjktMF9SQzIaAmVuIAEaBgiAnaC5Bg; S=billing-ui-v3=DfCy9fagxHBnp_k6Ahb2YxWacR-Tlcs1:billing-ui-v3-efe=DfCy9fagxHBnp_k6Ahb2YxWacR-Tlcs1:sso=ymwMsRF-vKj7nC3hpUBYStvs-69VEkx0; ADS_VISITOR_ID=00000000-0000-0000-0000-000000000000; SEARCH_SAMESITE=CgQIxJ4B; SID=g.a000zgjV6SjJHLUePm7_6K1u6mCsUSZe8MiuZmvyj_vmPHlgg8yzgtKdA9Q7Br9gUS2OjULqqwACgYKAdQSARISFQHGX2Mic7rOaO9P8U3OrSsC50MEFxoVAUF8yKqK1ULRrRe-fg5e2CI3tOh60076; __Secure-1PSID=g.a000zgjV6SjJHLUePm7_6K1u6mCsUSZe8MiuZmvyj_vmPHlgg8yz0dbeB3trjlAbtgb-KOMJggACgYKASsSARISFQHGX2Mi2DnbPpKYosfluOnfT4yRYRoVAUF8yKqyP9y02uPA_9OxFugXixjg0076; __Secure-3PSID=g.a000zgjV6SjJHLUePm7_6K1u6mCsUSZe8MiuZmvyj_vmPHlgg8yzEkob22f-Kb8fe9fbPA1slQACgYKATQSARISFQHGX2MiwrcwxNKG8mZZjotXufx9shoVAUF8yKoNizh7lCKGFCc4HALrR79l0076; HSID=A12tFNpCpNJ9yIl3j; SSID=AUxDo0Wyv7gTx4eU8; APISID=-bJNjJSeWoCfBZtx/Au5OyHdIYzvIhANzW; SAPISID=46Wq1QY2YFEJvp_-/ABGjuazXEO4Hvxg0C; __Secure-1PAPISID=46Wq1QY2YFEJvp_-/ABGjuazXEO4Hvxg0C; __Secure-3PAPISID=46Wq1QY2YFEJvp_-/ABGjuazXEO4Hvxg0C; OTZ=8190060_52_56_123900_52_436380; AEC=AVh_V2hU7IoRTPAaCgXrfoG5X4nM9bZrz0UD8rwIdayB4tfPR9zk1D1_7xc; NID=525=X1aOftCBVkJ2pq4I99S_5g2uSa_h-xlt10LCeP_j3Sz33BGTu-qHa0wKhvNhT-GoXO90gQwFFLkfeUUMtV12xcmzZIFFJkycpYwMt7H8wbv-Rbk9ab1mdzHakiX5Sr7552t4vBm7S5GhDJp8kyxrVGzU2frGytkOjY32HxVaO71cTav2g2qTCZIJOnEnmf-0UMvJYHQYmWuN2rQFQ2iV9xJO9-Z5QaQeI0Y-omxpkj8FFW41jIbLU_grEMngKIBvYONtRIxv2lZEZUuPTcKepwFkNnMwb_zmRd9ZaWa3aot6GuIrebcYk2JlIG8rYXpIHnSVzMvNdoUq4nR-APnU2uEoXEL9tecLi9j3Rpkg4T3gtB0DcxHn6oIRFbbwTlR-OuA4r5YYCseWfIZfslxZqG-XHt72d00pPID5W-NNkQ0KbMmkcy1mg7Dk1MRRWJtitAnkp4tClqYXxHcEJc968da1ChqbKIuqflhLLNBueGxDBofJ39zMLbrgTtpzBmX177BdufOtEuG4xOL-wVVFg-TdFCvydt-BNBIxhAwxJPZMlTRat4GMiscqMnTM7R54StCGB84ClYYjt-L9PRl-Xhlnnbo9RuaaySdwbC8SnzW1xq81e7YwBkfH8lrdSjtj76n35oID5HuvGunKyllprP7Ur-jyVUbrXtj153gGeXTeopAVLWMgfn-rjn18x8uwJy1hMFpd2SLcuQZ_oMViwIY5fCr5Db3jJ9R5UPRNe328z1OeTIGeYixsIzihz2iGbLa4ZtUkbPidBLNuf5hVDP_2OHiLua-h_G9--63rF5uUPsfeXOH3XhNaHa2zFnSp1R6h7_caiCjCgzAfJ6F4jIc778s0ySNgxZnu7KMj0jWPdWRma-Ef; __Secure-1PSIDTS=sidts-CjEB5H03P4rmd5l4G0lkKL0wZ0-1pjSz5rpa5EBkEGVoQgTNH-RF7Qr5OaXM-4_2Scs6EAA; __Secure-3PSIDTS=sidts-CjEB5H03P4rmd5l4G0lkKL0wZ0-1pjSz5rpa5EBkEGVoQgTNH-RF7Qr5OaXM-4_2Scs6EAA; DV=86TRsWX8cs9lACJ-bZgLX57NvaW-hpnJ1eQobKS9bwAAACAcuD9TMkTrQAAAABhFrO4c0K_MEAAAAAHw2_5TMtlDCwAAACKOl0gFWpkGBAAAAA; SIDCC=AKEyXzWYNxoPh0-m79tJd5Odt_sDVLR04MmA-hunAfWVQMcQ4cTN9mUhG8UQTg4eA-QgrjHiig; __Secure-1PSIDCC=AKEyXzWbNhq4Kqqm9qhATAixw9va-SOwsbYObkwzjgQhEBfn0Z3bV2yKVfuXQN3W884DOPSKVw; __Secure-3PSIDCC=AKEyXzUtoFjHmt3UmaHqzEbNl0WOllYvjeaG1NqKKBEMAnueYxzTc7a4a0knabNiVOhckzt2yws_",
    "referer": "https://www.google.com/",
    "sec-ch-prefers-color-scheme": "dark",
    "sec-ch-ua": '"Opera";v="120", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-arch": "",
    "sec-ch-ua-bitness": "64",
    "sec-ch-ua-form-factors": "",
    "sec-ch-ua-full-version": "120.0.5543.93",
    "sec-ch-ua-full-version-list": '"Opera";v="120.0.5543.93", "Not-A.Brand";v="8.0.0.0", "Chromium";v="135.0.7049.115"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-model": "Nexus 5",
    "sec-ch-ua-platform": "Android",
    "sec-ch-ua-platform-version": "6.0",
    "sec-ch-ua-wow64": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "x-client-data": "CM2KywE=",
}


headers_jobs = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=1, i",
    "referer": "https://www.google.com/",
    "sec-ch-prefers-color-scheme": "dark",
    "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-arch": '"arm"',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-form-factors": '"Desktop"',
    "sec-ch-ua-full-version": '"130.0.6723.58"',
    "sec-ch-ua-full-version-list": '"Chromium";v="130.0.6723.58", "Google Chrome";v="130.0.6723.58", "Not?A_Brand";v="99.0.0.0"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": '""',
    "sec-ch-ua-platform": '"macOS"',
    "sec-ch-ua-platform-version": '"15.0.1"',
    "sec-ch-ua-wow64": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
}

async_param = "_basejs:/xjs/_/js/k=xjs.s.en_US.JwveA-JiKmg.2018.O/am=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAACAAAoICAAAAAAAKMAfAAAAIAQAAAAAAAAAAAAACCAAAEJDAAACAAAAAGABAIAAARBAAABAAAAAgAgQAABAASKAfv8JAAABAAAAAAwAQAQACQAAAAAAcAEAQABoCAAAABAAAIABAACAAAAEAAAAFAAAAAAAAAAAAAAAAAAAAAAAAACAQADoBwAAAAAAAAAAAAAQBAAAAATQAAoACOAHAAAAAAAAAQAAAIIAAAA_ZAACAAAAAAAAcB8APB4wHFJ4AAAAAAAAAAAAAAAACECCYA5If0EACAAAAAAAAAAAAAAAAAAAUgRNXG4AMAE/dg=0/br=1/rs=ACT90oGxMeaFMCopIHq5tuQM-6_3M_VMjQ,_basecss:/xjs/_/ss/k=xjs.s.IwsGu62EDtU.L.B1.O/am=QOoQIAQAAAQAREADEBAAAAAAAAAAAAAAAAAAAAAgAQAAIAAAgAQAAAIAIAIAoEwCAADIC8AfsgEAawwAPkAAjgoAGAAAAAAAAEADAAAAAAIgAECHAAAAAAAAAAABAQAggAARQAAAQCEAAAAAIAAAABgAAAAAIAQIACCAAfB-AAFIQABoCEA_CgEAAIABAACEgHAEwwAEFQAM4CgAAAAAAAAAAAAACABCAAAAQEAAABAgAMCPAAA4AoE2BAEAggSAAIoAQAAAAAgAAAAACCAQAAAxEwA_ZAACAAAAAAAAAAkAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAQAEAAAAAAAAAAAAAAAAAAAAAQA/br=1/rs=ACT90oGZc36t3uUQkj0srnIvvbHjO2hgyg,_basecomb:/xjs/_/js/k=xjs.s.en_US.JwveA-JiKmg.2018.O/ck=xjs.s.IwsGu62EDtU.L.B1.O/am=QOoQIAQAAAQAREADEBAAAAAAAAAAAAAAAAAAAAAgAQAAIAAAgAQAAAKAIAoIqEwCAADIK8AfsgEAawwAPkAAjgoAGAAACCAAAEJDAAACAAIgAGCHAIAAARBAAABBAQAggAgRQABAQSOAfv8JIAABABgAAAwAYAQICSCAAfB-cAFIQABoCEA_ChEAAIABAACEgHAEwwAEFQAM4CgAAAAAAAAAAAAACABCAACAQEDoBxAgAMCPAAA4AoE2BAEAggTQAIoASOAHAAgAAAAACSAQAIIxEwA_ZAACAAAAAAAAcB8APB4wHFJ4AAAAAAAAAAAAAAAACECCYA5If0EACAAAAAAAAAAAAAAAAAAAUgRNXG4AMAE/d=1/ed=1/dg=0/br=1/ujg=1/rs=ACT90oFNLTjPzD_OAqhhtXwe2pg1T3WpBg,_fmt:prog,_id:fc_5FwaZ86OKsfdwN4P4La3yA4_2"
