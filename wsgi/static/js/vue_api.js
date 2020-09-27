
var temp_scr = {
    el: "#app"
};


temp_scr.data = {
    SCRfield: {
        name: "SCRfield",
        json: {
            state: {
                myid: 0,
                fid: 0,
                bid: 0,
                ids: [],
                interpreter: ""
            }
        }
    },
    SCRschedule: {
        name: "SCRschedule",
        json: []
    },
    SCRenv: {
        name: "SCRenv",
        json: {
            flag: "",
            gui: true,
            pulse_rate: 0,
            max_tid: 0,
            max_sub_process: 0,
            python: "",
            debug_mode: true,
            logger: {
                path: "log/",
                level: 1,
                console_stream: {
                    CRITICAL: true,
                    ERROR: true,
                    WARN: true,
                    INFO: true,
                    DEBUG: true,
                    NOTSET: true
                },
                log_file_out: {
                    CRITICAL: true,
                    ERROR: true,
                    WARN: true,
                    INFO: true,
                    DEBUG: true,
                    NOTSET: true
                },
                write_mode: "w"
            }
        }
    },
    SCRcodes: {
        name: "SCRcodes",
        json: [{
            folder_name: "",
            file_list: [],
        }]
    },
    disp: {
        data_view: true,
        schedule_change: false
    },
    code: {},
    form: {
        code_select: "wait",
        folder_select: 0
    },
    notification: []
};


temp_scr.methods = {
    $_ws_setup: function () {
        var __scr_ws = new WebSocket("ws://localhost:5016"); /* Don't publish ! */
        __scr_ws.onopen = function () {
            __scr_ws.send("start_server");
        };
        __scr_ws.onmessage = function (response) {
            scr.$_ws_get_data(response.data);
        }
    },
    $_ws_get_data: function (data) {
        if (data == "check") {
            return;
        };
        var json_data = JSON.parse(data);
        for (const key in json_data) {
            scr["SCR" + key].json = json_data[key];
        };
    },
    $_disp_change: function (display_name) {
        for (const key in this.disp) {
            this.disp[key] = false;
        };
        this.disp[display_name] = true;
    },
    $_receive_cmd: function (mode, index) {
        if (mode == "del") {
            this.SCRschedule.json[index].c = "delete_schedule";
            this.$_receive(this.SCRschedule.json[index]);
        } else if (mode == "add") {
            this.$_receive({
                sec: Number(this.form.sec),
                days1: false,
                c: "",
                d: {
                    lang: "python3",
                    file_path: this.SCRcodes.json[this.form.folder_select].folder_name,
                    file_name: this.form.code_select
                }
            });
        };
    },
    $_receive: function (json) {
        let params = new URLSearchParams();
        params.append("text", JSON.stringify(json));

        axios.post("http://localhost:5015/receive/", params) /* Don't publish ! */
            .then(response => {
                console.log("successful transmission: " + response.data);
            }).catch(error => {
                scr.notification.push({
                    message: error.data,
                    level: 1
                });
            });
    },
    $_write_local_conf: function (name) {
        this.$_receive({
            c: "local_conf",
            d: {
                file_path: name,
                data_key: this.code[name].data
            }
        });
    }
};


temp_scr.components = {
    "side-folder": Side_folder,
    "data-view-schedule": Data_view_schedule,
};