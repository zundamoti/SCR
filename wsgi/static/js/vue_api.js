var scr_api = new Vue({
  el: '#app',
  data: {
    SCRfield: {
      name: "SCRfield",
      json: {},
      raw: ""
    },
    SCRschedule: {
      name: "SCRschedule",
      json: {},
      raw: ""
    },
    SCRenv: {
      name: "SCRenv",
      json: {},
      raw: ""
    },
    SCRcodes: {
      name: "SCRcodes",
      json: [
        {
          folder_name: "",
          file_list: [],
        }
      ],
      raw: ""
    },
    disp: {
      data_view: true,
      schedule_change: false
    },
    form: {
      code_select:"wait",
      folder_select: 0
    }
  },
  methods: {
    ws_setup: function (display_name) {
      ws = new WebSocket("ws://localhost:5016");
      ws.onopen = function () {
        ws.send('start_server');
      };
      ws.onmessage = function (res) {
        scr_api.ws_get_data(res.data);
      }
    },
    ws_get_data: function (data) {
      if(data == 'check'){
        return;
      };
      json_data = JSON.parse(data);
      for (const key in json_data) {
        scr_api['SCR' + key].json = json_data[key];
        scr_api['SCR' + key].raw = JSON.stringify(scr_api['SCR' + key].json, null, 4);
      }
      scr_api.ws = scr_api.ws + data;
    },
    disp_change: function (display_name) {
      for (key in this.disp) {
          this.disp[key] = false;
      }
      this.disp[display_name] = true;
    },
    receive_cmd: function (mode,index,cmd) {
      if(mode == "del"){
        send_json = this.SCRschedule.json[index];
        send_json.c = cmd;

      } else if(mode == "add"){
        send_json = {};
        send_json["sec"] = Number(this.form.sec);
        send_json["days1"] = false,
        send_json["c"] = "";

        details = {
          "lang": "python3",
          "file_path": this.SCRcodes.json[this.form.folder_select].folder_name,
          "file_name": this.form.code_select
        };
        
        send_json['d'] = details;
      };
      this.receive(send_json);
    },
    write_local_conf: function (name) {
      send_json = {};
      send_json["c"] = "local_conf";
      details = {
        "file_path": name,
        "data_key": this[name].data
      };
      send_json['d'] = details;
      this.receive(send_json);
    },
    receive: function (json) {

      let params = new URLSearchParams();
      params.append('text', JSON.stringify(json));
      
      axios.post('/receive/', params)
        .then(response => {
          console.log('send comp: ' + response.data.text);
        }).catch(error => {
          console.log(error);
        });


    }
  },
  components: {
    'side-folder': Side_folder,
    'side-redis': Side_redis,
    'data-view': Data_view,
    'data-view-schedule': Data_view_schedule,
    'data-view-field': Data_view_field
  }
});

