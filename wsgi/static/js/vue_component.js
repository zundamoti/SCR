


var Data_view = {
    props: ['value'],
    template: `
    <div class="data-view">
        <h3>{{ value.name }}</h3>
        <div class="json code-block-wrapper">
            <pre><code>{{ value.raw }}</code></pre>
        </div>
    </div>
    `
};

var Data_view_field = {
    props: ['field'],
    template: `
    <div class="row">
        <p>myid:{{field.json.state.myid}} fid:{{field.json.state.fid}}</p>
    </div>
    `
};

var Data_view_schedule = {
    props: ['sc', 'index'],
    template: `
        <div class="row">
            <p><label>file :</label> {{ sc.d.file_path }} / {{ sc.d.file_name }} <label>sec :</label> {{ sc.sec }}</p>
            <div class="button" v-on:click="receive_cmd('del', index )">del</div>
        </div>
    `,
    methods: {
        receive_cmd: function (mode,index) {
            scr_api.receive_cmd(mode,index,'delete_schedule');
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

var Side_redis = {
    props: ['value'],
    template: `
    <div class="sideitem">
        <object type="image/svg+xml" data="/static/assets/menu.svg" width="24" height="24"></object>
    </div>
    `
};



