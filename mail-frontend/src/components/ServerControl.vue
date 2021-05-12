<template>
    <section class="main">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-rank"></i> 服务器管理</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-row :gutter="20">
                整体服务器启停
                 <el-divider></el-divider>
                <el-col :span="5">
                    <div class="container">
                        <p>启动SMTP与POP3服务</p>
                        <br>
                        <el-button type="success" @click="startServer">启动</el-button>
                    </div>
                </el-col>
                <el-col :span="5">
                    <div class="container">
                        <p>暂停SMTP与POP3服务</p>
                        <br>
                        <el-button type="danger" @click="stopServer">暂停</el-button>
                    </div>
                </el-col>
                <el-col :span="5">
                    <div class="container">
                        <p>重启SMTP与POP3服务</p>
                        <br>
                        <el-button type="primary" @click="restartServer">重启</el-button>
                    </div>
                </el-col>
            </el-row>
        </div>
        <br>
        <div class="container">
            <el-row :gutter="20">
                SMTP服务器启停
                 <el-divider></el-divider>
                <el-col :span="5">
                    <div class="container">
                        <p>启动SMTP服务</p>
                        <br>
                        <el-button type="success" @click="startSmtp">启动</el-button>
                    </div>
                </el-col>
                <el-col :span="5">
                    <div class="container">
                        <p>暂停SMTP服务</p>
                        <br>
                        <el-button type="danger" @click="stopSmtp">暂停</el-button>
                    </div>
                </el-col>
                <el-col :span="5">
                    <div class="container">
                        <p>重启SMTP服务</p>
                        <br>
                        <el-button type="primary" @click="restartSmtp">重启</el-button>
                    </div>
                </el-col>
            </el-row>
        </div>
        <br>
        <div class="container">
            <el-row :gutter="20">
                POP3服务器启停
                 <el-divider></el-divider>
                <el-col :span="5">
                    <div class="container">
                        <p>启动POP3服务</p>
                        <br>
                        <el-button type="success" @click="startPop3">启动</el-button>
                    </div>
                </el-col>
                <el-col :span="5">
                    <div class="container">
                        <p>暂停POP3服务</p>
                        <br>
                        <el-button type="danger" @click="stopPop3">暂停</el-button>
                    </div>
                </el-col>
                <el-col :span="5">
                    <div class="container">
                        <p>重启POP3服务</p>
                        <br>
                        <el-button type="primary" @click="restartPop3">重启</el-button>
                    </div>
                </el-col>
            </el-row>
        </div>
        <!-- <el-dialog v-dialogDrag title="拖拽弹框" center :visible.sync="visible" width="30%">
            我是一个可以拖拽的对话框！
            <span slot="footer" class="dialog-footer">
                <el-button @click="visible = false">取 消</el-button>
                <el-button type="primary" @click="visible = false">确 定</el-button>
            </span>
        </el-dialog> -->
    </section>
</template>

<script>
import Axios from 'axios'
export default {
    data(){
        return {
            visible: false,
            method: "",
            type:""
        }
    },
    methods: {
        serverControl() {            
            let requestURL = "";
            if (this.type === "smtp")
            {
                requestURL = '/apis/webmail/controlSmtp/'
            }
            else if (this.type === "pop3")
            {
                requestURL = '/apis/webmail/controlPop3/';
            }
            
            let data = new FormData();
            data.append("method",this.method)
            data.append("authorityValue",localStorage.getItem('authorityValue'))
            Axios
                .post(requestURL,data)
                .then(response => {
                    // console.log(JSON.stringify(response));
                    if (response.data.status == 200)
                    {
                        this.$message({
                            type: 'success',
                            message: '操作成功'
                        })
                    }
                    else
                    {
                        this.$message({
                            type: 'error',
                            message: '未能连接到服务器或服务器出错'
                        })
                    }
                })
                .catch((err) => {
                    // console.log(err);
                    this.$message({
                        type: 'error',
                        message: '未能连接到服务器或服务器出错'
                    })
                })
            this.method = "";
            this.type = "";
        },
        startServer() {
            this.$confirm('确定要启动邮件服务器吗？','提示',{
                type: 'warning'
            })
            .then(() =>{
                this.method = "start";
                this.type = "smtp";
                this.serverControl();
                this.method = "start";
                this.type = "pop3";
                this.serverControl();
            })
            .catch((err) =>{
                // console.log(err);
                this.$message({
                    type: 'info',
                    message: '操作已取消'
                })
            })
        },
        stopServer() {
            this.$confirm('确定要暂停邮件服务器吗？','提示',{
                type: 'warning'
            })
            .then(() =>{
                this.method = "stop";
                this.type = "smtp";
                this.serverControl();
                this.method = "stop";
                this.type = "pop3";
                this.serverControl();
            })
            .catch((err) =>{
                // console.log(err);
                this.$message({
                    type: 'info',
                    message: '操作已取消'
                })
            })
        },
        restartServer() {
            this.$confirm('确定要重新启动邮件服务器吗？','提示',{
                type: 'warning'
            })
            .then(() =>{
                this.method = "restart";
                this.type = "smtp";
                this.serverControl();
                this.method = "restart";
                this.type = "pop3";
                this.serverControl();
            })
            .catch((err) =>{
                // console.log(err);
                this.$message({
                    type: 'info',
                    message: '操作已取消'
                })
            })
        },
        startSmtp() {
            this.$confirm('确定要启动smtp服务器吗？','提示',{
                type: 'warning'
            })
            .then(() =>{
                this.method = "start";
                this.type = "smtp";
                this.serverControl();
            })
            .catch((err) =>{
                // console.log(err);
                this.$message({
                    type: 'info',
                    message: '操作已取消'
                })
            })
        },
        stopSmtp() {
            this.$confirm('确定要暂停smtp服务器吗？','提示',{
                type: 'warning'
            })
            .then(() =>{
                this.method = "stop";
                this.type = "smtp";
                this.serverControl();
            })
            .catch((err) =>{
                // console.log(err);
                this.$message({
                    type: 'info',
                    message: '操作已取消'
                })
            })
        },
        restartSmtp() {
            this.$confirm('确定要重新启动smtp服务器吗？','提示',{
                type: 'warning'
            })
            .then(() =>{
                this.method = "restart";
                this.type = "smtp";
                this.serverControl();
            })
            .catch((err) =>{
                // console.log(err);
                this.$message({
                    type: 'info',
                    message: '操作已取消'
                })
            })
        },
        startPop3() {
            this.$confirm('确定要启动pop3服务器吗？','提示',{
                type: 'warning'
            })
            .then(() =>{
                this.method = "start";
                this.type = "pop3";
                this.serverControl();
            })
            .catch((err) =>{
                // console.log(err);
                this.$message({
                    type: 'info',
                    message: '操作已取消'
                })
            })
        },
        stopPop3() {
            this.$confirm('确定要暂停pop3服务器吗？','提示',{
                type: 'warning'
            })
            .then(() =>{
                this.method = "stop";
                this.type = "pop3";
                this.serverControl();
            })
            .catch((err) =>{
                // console.log(err);
                this.$message({
                    type: 'info',
                    message: '操作已取消'
                })
            })
        },
        restartPop3() {
            this.$confirm('确定要重启pop3服务器吗？','提示',{
                type: 'warning'
            })
            .then(() =>{
                this.method = "restart";
                this.type = "pop3";
                this.serverControl();
            })
            .catch((err) =>{
                // console.log(err);
                this.$message({
                    type: 'info',
                    message: '操作已取消'
                })
            })
        },
    },
}
</script>

<style>

</style>
