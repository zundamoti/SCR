SCR = {
    "flag": "none",
    "gui": True,
    "pulse_rate": 0.1,
    "max_tid": 0,
    "max_sub_process": 2,
    "python": "python3",
    "debug_mode": True,
    "logger":{
        "path": "log/",
        "level": 1,
        "console_stream": {
            "CRITICAL": True,
            "ERROR": True,
            "WARN": True,
            "INFO": True,
            "DEBUG": True,
            "NOTSET": True
        },
        "log_file_out": {
            "CRITICAL": True,
            "ERROR": True,
            "WARN": True,
            "INFO": False,
            "DEBUG": False,
            "NOTSET": False
        },
        "write_mode": "w"

    }
}

GUI = {
    "address": "localhost",
    "wsgi_port": 5015,
    "web_socket_port": 5016,
    "web_socket_pulse_rate": 0.3,
    "web_socket_wait_rate": 3,
    "GUIraw": {
        "field": False,
        "schedule": "",
        "env": "",
        "codes": ""
    }
}

REDIS = {
    "address": '0.0.0.0',
    "port": 6379,
    "db": 0
}


SCRCTL = {
    "code_exec":{
        "py": "python3"
    }
}

DEFAULT_FIELD = {
    "state": {
        "myid": 0,
        "fid": 0,
        "bid": 0,
        "ids": [],
        "interpreter": "cmd",
        "ssh": [
            {
                "name": "example",
                "details":{
                    "public_key": "abcdef",
                    "HOST": '192.168.1.*',
                    "PORT": '22',
                    "USER": 'user',
                    "KEY_PATH": '/HOME~~~',
                    "PASSWORD": 'password'
                }
            }
        ]
    },
    "meta": {
        "near_field": [],
        "near_field_path": []
    },
    "docker": {
        "images":[
            {
                "image_id":"",
                "image_name":"",
                "image_tag":"",
                "image_created":"",
                "image_size":""
            }
        ],
        "containers":[
            {
                
            }
        ]
    }
}

DEFAULT_RECEIVE = {
    "sec": 0,
    "days1": False,
    "c": False,
}

DEFAULT_DETAILS ={
    "d": {
        "priority": 0,
        "lang":"",
        "data_key":"",
        "file_path":"",
        "file_name":"",
    }
}