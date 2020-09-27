


var Data_view_schedule = {
    props: ['sc', 'index'],
    template: `
        <div class="row">
            <p><label>file :</label> {{ sc.d.file_path }} / {{ sc.d.file_name }} <label>sec :</label> {{ sc.sec }}</p>
            <div class="button" v-on:click="$_c_receive_cmd('del', index )">del</div>
        </div>
    `,
    methods: {
        $_c_receive_cmd: function (mode,index) {
            scr.$_receive_cmd(mode,index);
          }
    }
};

var Side_folder = {
    props: ['value'],
    template: `
    <div class="sideitem">
        <object type="image/svg+xml" data="/static/assets/folder.svg" width="24" height="24"></object>
    </div>
    `
};



