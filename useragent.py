import random


class UserAgent:
    def __init__(self):
        generated = []

        self.browserVersions = ["Mozilla/4.0", "Mozilla/5.0", "Dalvik/1.6.0", "Dalvik/2.1.0", "Apache-HttpClient/4.5.13", "GuzzleHttp/6.3.3", "curl/7.68.0", "PHP/7.4.6", "WordPress/5.6.2", "Opera/9.60"]
        self.systemInformations = ["Linux; Android 9; SM-G9550", "Linux; Android 11; GM1913", "Linux; Android 8.1.0; Flare_Y3", "Linux; Android 9; SAMSUNG SM-A505F", "Linux; Android 7.0; Wieppo S6", "Linux; Android 9; SAMSUNG SM-G950W", "Linux; U; Android 4.4.2; GA-TAB7V3G Build/KOT49H", "Linux; Android 8.1.0; DUB-LX1 Build/HUAWEIDUB-LX1; wv", "Linux; Android 7.1.1; ONEPLUS A5000 Build/NMF26X", "Linux; U; Android 11; SM-M307FN Build/RP1A.200720.012", "Windows NT 6.1;", "Linux; Android 9; JAT-LX1 Build/HONORJAT-LX1", "Windows NT 6.3; Win64; x64", "Linux; U; Android 10; PCDM10 Build/QP1A.190711.020", "Linux; Android 7.0; IFP5550-2_VS17583_BE2 Build/NRD90M; wv", "Macintosh; Intel Mac OS X 10_15_6", "Macintosh; Intel Mac OS X 10_15_5", "Linux; Android 11; moto g stylus (XT2115DL)", "iPad; CPU OS 13_4 like Mac OS X", "iPad; CPU OS 13_7 like Mac OS X", "iPad; CPU OS 14_4 like Mac OS X", "Linux; Android 9; Hisense Infinity H30", "Linux; U; Android 4.2.2; HUAWEI Y511-T00 Build/HUAWEIY511-T00", "Linux; U; Android 5.1.1; vivo X6S A Build/LMY47V", "iPhone; CPU iPhone OS 14_4 like Mac OS X", "Linux; U; Android 10; Mi Note 10 Lite MIUI/V11.0.1.0.QFNRUXM", "Linux; arm_64; Android 9; ONEPLUS A3003", "Linux; U; Android 10; moto g(7) play Build/QPYS30.52-22-2", "Linux; Android 7.1.1; Lenovo K8 Plus", "Linux; Android 10; ONEPLUS A6013 Build/QKQ1.190716.003; wv", "Linux; Android 11; SM-T720", "iPhone; CPU iPhone OS 13_3_1 like Mac OS X", "iPhone; iOS 12.4.7; en_FR", "Linux; Android 7.0; ELUGA I4", "Linux; Android 9; ZTE Blade A3 Lite", "Linux; Android 7.0; SAMSUNG SM-J530F", "Linux; U; Android 8.1.0; MI 5X MIUI/9.3.7", "Linux; U; Android 6.0; Tecno K18 Build/TecnoK18", "X11; Linux x86_64", "Windows 98"]
        self.Platform = ["AppleWebKit/537.36", "Chrome/85.0.4183.127", "Chrome/87.0.4280.38", "Chrome/87.0.4280.101", "Chrome/89.0.4389.86", "SamsungBrowser/12.0", "SamsungBrowser/13.2", "Chrome/70.0.3538.110", "Chrome/88.0.4324.152", "Chrome/93.0.4577.82", "Java/11.0.12"]
        self.PlatformDetails = ["KHTML, like Gecko"]
        self.Extensions = ["Mobile", "Viber/13.2.0.8", "Safari/537.36", "Version/4.0", "Version/4.1", "Presto/2.10.285", "Version/11.00"]

        self.generated = generated

    def shake(self, max:int=1000, new:bool=True):
        if new:
            self.generated.clear()

        def get_random(lst:list):
            return random.choice(lst)

        for i in range(max):
            rand = f"{get_random(self.browserVersions)} ({get_random(self.systemInformations)}) {get_random(self.Platform)} ({get_random(self.PlatformDetails)}) {get_random(self.Extensions)}"
            if not rand in self.generated:
                self.generated.append(rand)
            # '\r', len(self.generated).__str__() + "/" + str(i)

    def get(self):
        if len(self.generated) == 0:
            self.shake()
        return random.choice(self.generated)

    class Devices:
        ua_platform_based = {
            'samsung_galaxy_s22': 'Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36',
            'samsung_galaxy_s21': 'Mozilla/5.0 (Linux; Android 10; SM-G996U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
            'samsung_galaxy_s20': 'Mozilla/5.0 (Linux; Android 10; SM-G980F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.96 Mobile Safari/537.36',
            'samsung_galaxy_s10': 'Mozilla/5.0 (Linux; Android 9; SM-G973U Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
            'samsung_galaxy_s9': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
            'samsung_galaxy_s8': 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36',
            'samsung_galaxy_s7': 'Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36',
            'samsung_galaxy_s7_edge': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36',
            'samsung_galaxy_s6': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36',
            'samsung_galaxy_s6_edge_plus': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36',
            'google_pixel_6': 'Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36',
            'google_pixel_5': 'Mozilla/5.0 (Linux; Android 11; Pixel 5 Build/RQ3A.210805.001.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36',
            'google_pixel_4': 'Mozilla/5.0 (Linux; Android 10; Google Pixel 4 Build/QD1A.190821.014.C2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36',
            'google_pixel_3': 'Mozilla/5.0 (Linux; Android 10; Google Pixel 4 Build/QD1A.190821.014.C2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36',
            'google_pixel_2': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 Build/OPD1.170811.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
            'google_pixel': 'Mozilla/5.0 (Linux; Android 7.1.1; Google Pixel Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/54.0.2840.85 Mobile Safari/537.36',
            'nexus_6p': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36',
            'sony_xperia_1': 'Mozilla/5.0 (Linux; Android 9; J8110 Build/55.0.A.0.552; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36',
            'sony_xperia_xz': 'Mozilla/5.0 (Linux; Android 7.1.1; G8231 Build/41.2.A.0.219; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
            'sony_xperia_z5': 'Mozilla/5.0 (Linux; Android 6.0.1; E6653 Build/32.2.A.0.253) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36',
            'htc_desire_21_pro_5g': 'Mozilla/5.0 (Linux; Android 10; HTC Desire 21 pro 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
            'htc_u20_5g': 'Mozilla/5.0 (Linux; Android 10; Wildfire U20 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36',
            'htc_one_x10': 'Mozilla/5.0 (Linux; Android 6.0; HTC One X10 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36',
            'htc_one_m9': 'Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.3',
            'apple_iphone_se_(3rd_generation)': 'Mozilla/5.0 (iPhone14,6; U; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19E241 Safari/602.1',
            'iphone_13_pro_max': 'Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1',
            'iphone_12': 'Mozilla/5.0 (iPhone13,2; U; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1',
            'iphone_11': 'Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1',
            'apple_iphone_xr_(safari)': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
            'apple_iphone_xs_(chrome)': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1',
            'apple_iphone_xs_max_(firefox)': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15',
            'apple_iphone_x': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'apple_iphone_8': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
            'apple_iphone_8_plus': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5370a Safari/604.1',
            'apple_iphone_7': 'Mozilla/5.0 (iPhone9,3; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1',
            'apple_iphone_7_plus': 'Mozilla/5.0 (iPhone9,4; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1',
            'apple_iphone_6': 'Mozilla/5.0 (Apple-iPhone7C2/1202.466; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3',
            'microsoft_lumia_650': 'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254',
            'microsoft_lumia_550': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; RM-1127_16056) AppleWebKit/537.36(KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10536',
            'microsoft_lumia_950': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.1058',
            'samsung_galaxy_tab_s8_ultra': 'Mozilla/5.0 (Linux; Android 12; SM-X906C Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36',
            'lenovo_yoga_tab_11': 'Mozilla/5.0 (Linux; Android 11; Lenovo YT-J706X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'google_pixel_c': 'Mozilla/5.0 (Linux; Android 7.0; Pixel C Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36',
            'sony_xperia_z4_tablet': 'Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36',
            'nvidia_shield_tablet_k1': 'Mozilla/5.0 (Linux; Android 6.0.1; SHIELD Tablet K1 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Safari/537.36',
            'samsung_galaxy_tab_s3': 'Mozilla/5.0 (Linux; Android 7.0; SM-T827R4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Safari/537.36',
            'samsung_galaxy_tab_a': 'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36',
            'amazon_kindle_fire_hdx_7': 'Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/47.1.79 like Chrome/47.0.2526.80 Safari/537.36',
            'lg_g_pad_7.0': 'Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36',
            'windows_10-based_pc_using_edge_browser': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
            'chrome_os-based_laptop_using_chrome_browser_(chromebook)': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'mac_os_x-based_computer_using_a_safari_browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
            'windows_7-based_pc_using_a_chrome_browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
            'linux-based_pc_using_a_firefox_browser': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
            'google_adt-2': 'Dalvik/2.1.0 (Linux; U; Android 9; ADT-2 Build/PTT5.181126.002)',
            'chromecast': 'Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.0 Safari/537.36',
            'roku_ultra': 'Roku4640X/DVP-7.70 (297.70E04154A)',
            'minix_neo_x5': 'Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
            'amazon_aftwmst22': 'Mozilla/5.0 (Linux; Android 9; AFTWMST22 Build/PS7233; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.152 Mobile Safari/537.36',
            'amazon_4k_fire_tv': 'Mozilla/5.0 (Linux; Android 5.1; AFTS Build/LMY47O) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/41.99900.2250.0242 Safari/537.36',
            'google_nexus_player': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus Player Build/MMB29T)',
            'apple_tv_6th_gen_4k': 'AppleTV11,1/11.1',
            'apple_tv_5th_gen_4k': 'AppleTV6,2/11.1',
            'apple_tv_4th_gen': 'AppleTV5,3/9.1.1',
            'playstation_5': 'Mozilla/5.0 (PlayStation; PlayStation 5/2.26) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15',
            'playstation_4': 'Mozilla/5.0 (PlayStation 4 3.11) AppleWebKit/537.73 (KHTML, like Gecko)',
            'playstation_vita': 'Mozilla/5.0 (PlayStation Vita 3.61) AppleWebKit/537.73 (KHTML, like Gecko) Silk/3.2',
            'xbox_series_x': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox Series X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36 Edge/20.02',
            'xbox_one_s': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; XBOX_ONE_ED) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
            'xbox_one': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.10586',
            'nintendo_switch': 'Mozilla/5.0 (Nintendo Switch; WifiWebAuthApplet) AppleWebKit/601.6 (KHTML, like Gecko) NF/4.0.0.5.10 NintendoBrowser/5.1.0.13343',
            'nintendo_wii_u': 'Mozilla/5.0 (Nintendo WiiU) AppleWebKit/536.30 (KHTML, like Gecko) NX/3.0.4.2.12 NintendoBrowser/4.3.1.11264.US',
            'nintendo_3ds': 'Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU',
            # 'google_bot': 'Mozilla/5.0 (compatible; Googlebot/2.1;)',
            # 'bing_bot': 'Mozilla/5.0 (compatible; bingbot/2.0;)',
            # 'yahoo!_bot': 'Mozilla/5.0 (compatible; Yahoo! Slurp;)',
            'amazon_kindle_4': 'Mozilla/5.0 (X11; U; Linux armv7l like Android; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/533.2+ Kindle/3.0+',
            'amazon_kindle_3': 'Mozilla/5.0 (Linux; U; en-US) AppleWebKit/528.5+ (KHTML, like Gecko, Safari/528.5+) Version/4.0 Kindle/3.0 (screen 600x800; rotate)'
        }
        def random(self):
            return random.choice(list(self.ua_platform_based.values()))

        def all(self) -> list:
            return list(self.ua_platform_based.keys())
        def get(self, device:str) -> str:
            if device in self.ua_platform_based:
                return self.ua_platform_based[device]
            else:
                return ''
        def put(self, device:str, useragent) -> None:
            if device not in self.ua_platform_based:
                self.ua_platform_based[device] = useragent
        def delete(self, device:str) -> None:
            if device in self.ua_platform_based:
                del self.ua_platform_based[device]

Useragent = UserAgent()