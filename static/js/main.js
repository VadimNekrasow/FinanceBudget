var app_new_operation = new Vue({
    el: "#app_new_operation",
    data: {
        state_radio: 0,
        options: [],
    },

    created(){
        var request = sendRequest('/?type_pay=' + this.state_radio + '', 'get').then((response)=>{
            this.options = response.data.categories;
        })
    },

    methods: {
        radio_changed(){
            var request = sendRequest('/?type_pay=' + this.state_radio + '', 'get').then((response)=>{
            this.options = response.data.categories;
            })
        }
    }
});

var app_update_operation = new Vue({
    el: '#app_update_operation',
    data: {
        state_radio: 0,
        options: [],
        instance: 0,
    },
    created(){
        this.state_radio = document.getElementById('type_pay').value;
        this.instance = document.getElementById('instance').value;
        var request = sendRequest('/?type_pay=' + this.state_radio + '', 'get').then((response)=>{
            this.options = response.data.categories;
        })
    },
     methods: {
        radio_changed(){
            var request = sendRequest('/?type_pay=' + this.state_radio + '', 'get').then((response)=>{
            this.options = response.data.categories;
            console.log(response.data.categories);
            })
        },
    },

});

var app_category = new Vue({
    el: '#app_category',
    methods: {
        delete_category(id, name){
            sendRequest('/ajax/'+id+'/delete/', 'post').then((response)=>{
                console.log(response.data)
                if (response.data.result == 'ok'){
                    location.reload();
                }
            });
        },

        delete_operation(id, url){
            sendRequest(url, 'post').then((response)=>{
                console.log(response.data)
                if (response.data.result == 'ok'){
                    location.reload();
                }
            });
        }
    }
});


var app_statistic = new Vue({
    el: '#app-statistic',
    data: {
        state_calendar: 0,
        state_radio: 0,
        chart: null,
    },
    methods: {
        current_date(){
            var now = new Date();
            return (now.toLocaleString("en-US", {year: 'numeric'}) + '-' +now.toLocaleString("en-US", {month: '2-digit'}));
        },
        current_year(){
            var now = new Date();
            return (now.toLocaleString('en-Us', {year: 'numeric'}));
        },

        create_chart(){
            var ctx = document.getElementById('chart')//.getContext('2d');
            this.chart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: [],
                    datasets: [{
                        label: '',
                        data: [],
                        backgroundColor: [],
                }]},
            });
            this.update_chart();
        },

        radio_changed(){
            this.update_chart();
        },

        type_date_changed(){

        },

        update_chart(){
            sendRequest('/ajax/chart?type_pay=' + this.state_radio + '', 'get').then((response)=>{
                this.chart.data.labels = [];
                this.chart.data.datasets[0].data = [];
                this.chart.data.datasets[0].backgroundColor = [];

                for (var item in response.data.data){
                    item = response.data.data[item]
                    this.chart.data.labels.push(item.category__name);
                    this.chart.data.datasets[0].data.push(parseFloat(item.total));
                    this.chart.data.datasets[0].backgroundColor.push(item.color);
                }

                this.chart.update();

            });
        },
    },
    mounted(){
        this.create_chart();
    }

});

function sendRequest(url, method, data){
    var request = axios({
        method: method,
        url: url,
        data: data,
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    return request
}

function month_change(value, url){
    atrs = value.split('-');
    document.location.href = url+'?year=' + atrs[0] + '&month=' + atrs[1];
}

function click_on_link(url){
    document.location.href = url;
}



