<template>
    <div v-loading="loading">
        <el-row :gutter="20">
            <el-col :span="8">
                <el-card shadow="hover" class="mgb20" style="height:180px;">
                    <div class="user-info">
                        <div class="user-info-cont">
                            <div class="user-info-name">{{name}}</div>
                        </div>
                    </div>
                    <div>{{role}}</div>
                </el-card>
            </el-col>
            <el-col :span="16">
                <el-col :span='8'>
                    <el-card shadow="hover" :body-style="{padding: '0px'}">
                        <div class="grid-content grid-con-1">
                            <i class="el-icon-lx-people grid-con-icon"></i>
                            <div class="grid-cont-right">
                                <div class="grid-num">{{ userNum }}</div>
                                <div>用户总量</div>
                            </div>
                        </div>
                    </el-card>
                </el-col>
                <el-col :span='8'>
                    <el-card shadow="hover" :body-style="{padding: '0px'}">
                        <div class="grid-content grid-con-2">
                            <i class="el-icon-lx-mail grid-con-icon"></i>
                            <div class="grid-cont-right">
                                <div class="grid-num">{{ mailNum }}</div>
                                <div>邮件总数</div>
                            </div>
                        </div>
                    </el-card>
                </el-col>
                <el-col :span='8'>
                    <el-card shadow="hover" :body-style="{padding: '0px'}">
                        <div class="grid-content grid-con-3">
                            <i class="el-icon-lx-time grid-con-icon"></i>
                            <div class="grid-cont-right">
                                <div class="grid-num" style="white-space: pre-line">{{ nowDatetime}}</div>
                            </div>
                        </div>
                    </el-card>
                </el-col>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="12">
                <el-card shadow="hover">
                    <schart ref="bar" class="schart" canvasId="bar" :options="options"></schart>
                </el-card>
            </el-col>
            <el-col :span="12">
                <el-card shadow="hover">
                    <schart ref="line" class="schart" canvasId="line" :options="options2"></schart>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import Schart from 'vue-schart';
import bus from './common/bus';
import Axios from 'axios'
export default {
    name: 'dashboard',
    data() {
        return {
            name: localStorage.getItem('userName'),
            authority: localStorage.getItem('authorityValue'),
            todoList: [
                {
                    title: '今天要修复100个bug',
                    status: false
                },
                {
                    title: '今天要修复100个bug',
                    status: false
                },
                {
                    title: '今天要写100行代码加几个bug吧',
                    status: false
                },
                {
                    title: '今天要修复100个bug',
                    status: false
                },
                {
                    title: '今天要修复100个bug',
                    status: true
                },
                {
                    title: '今天要写100行代码加几个bug吧',
                    status: true
                }
            ],
            options: {
                type: 'bar',
                title: {
                    text: '最近一周邮件量图'
                },
                xRorate: 25,
                labels: [],
                datasets: []
            },
            options2: {
                type: 'line',
                title: {
                    text: '最近五个月新增用户数图'
                },
                labels: [],
                datasets: []
            },
            userNum: 0,
            mailNum: 0,
            nowDatetime: "",
            userInfos: [],
            mailInfos: [],
            loading: false
        };
    },
    components: {
        Schart
    },
    computed: {
        role() {
            return this.authority === '1' ? '管理员' : '超级管理员';
        }
    },
    mounted() {
        this.setTime(1000);
    },
    created() {
        this.getData();
        this.setTime(0);
    },
    methods: {
        setTime(timespan) {
            setInterval(this.getDatetime,timespan);
        },
        getDatetime() {
            let myDate = new Date();
            
            this.nowDatetime = 
                myDate.toLocaleDateString() + "\n" + 
                myDate.toLocaleTimeString()
        },
        changeDate() {
            const now = new Date().getTime();
            this.data.forEach((item, index) => {
                const date = new Date(now - (6 - index) * 86400000);
                item.name = `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`;
            });
        },
        getData() {
            this.loading = true;
            let requestURL = "/apis/webmail/users";
            Axios
                .get(requestURL)
                .then(response => {
                    this.userNum = response.data.data.length;
                })
                .catch((err) => {
                    this.$message.error("获取数据失败");
                })
            
            requestURL = "/apis/webmail/mails/";
            Axios
                .get(requestURL)
                .then(response => {
                    this.mailNum = response.data.length;
                })
                .catch((err) => {
                    this.$message.error("获取数据失败");
                })

            requestURL = "/apis/webmail/getmailstatic/"
            Axios
                .post(requestURL)
                .then(response => {
                    this.mailInfos = JSON.parse(response.data.data);
                    this.options.datasets.push({
                        "label": "邮件数",
                        "data": []
                    });
                    for (let i=0;i<this.mailInfos.length;i++)
                    {
                        this.options.labels.push(this.mailInfos[i].date);
                        this.options.datasets[0].data.push(this.mailInfos[i].mailCount);
                    }
                })
                .catch((err) => {
                    this.$message.error("获取数据失败");
                })

            requestURL = "/apis/webmail/getuserstatic/"
            Axios
                .post(requestURL)
                .then(response => {
                    this.userInfos = JSON.parse(response.data.data);
                    this.options2.datasets.push({
                        "label": "用户数",
                        "data": []
                    });
                    for (let i=0;i<this.userInfos.length;i++)
                    {
                        this.options2.labels.push(this.userInfos[i].date);
                        this.options2.datasets[0].data.push(this.userInfos[i].userCount);
                    }
                })
                .catch((err) => {
                    this.$message.error("获取数据失败");
                })

            setTimeout(() => {
                this.loading = false;
            }, 1000);
        }   
    }
};
</script>


<style scoped>
.el-row {
    margin-bottom: 20px;
}

.grid-content {
    display: flex;
    align-items: center;
    height: 100px;
}

.grid-cont-right {
    flex: 1;
    text-align: center;
    font-size: 14px;
    color: #999;
}

.grid-num {
    font-size: 30px;
    font-weight: bold;
}

.grid-con-icon {
    font-size: 50px;
    width: 100px;
    height: 100px;
    text-align: center;
    line-height: 100px;
    color: #fff;
}

.grid-con-1 .grid-con-icon {
    background: rgb(45, 140, 240);
}

.grid-con-1 .grid-num {
    color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
    background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
    color: rgb(45, 140, 240);
}

.grid-con-3 .grid-con-icon {
    background: rgb(242, 94, 67);
}

.grid-con-3 .grid-num {
    color: rgb(242, 94, 67);
}

.user-info {
    display: flex;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 2px solid #ccc;
    margin-bottom: 20px;
}

.user-info-cont {
    padding-left: 40px;
    flex: 1;
    font-size: 14px;
    color: #999;
}

.user-info-cont div:first-child {
    font-size: 30px;
    color: #222;
}

.mgb20 div:nth-child(2) {
    padding-left: 50%;
}

.user-info-list {
    font-size: 14px;
    color: #999;
    line-height: 25px;
}

.user-info-list span {
    margin-left: 70px;
}

.mgb20 {
    margin-bottom: 20px;
}

.todo-item {
    font-size: 14px;
}

.todo-item-del {
    text-decoration: line-through;
    color: #999;
}

.schart {
    width: 100%;
    height: 300px;
}
</style>
