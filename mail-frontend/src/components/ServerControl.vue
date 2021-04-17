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
                        <el-button type="success" @click="visible = true;">启动</el-button>
                    </div>
                </el-col>
                <el-col :span="5">
                    <div class="container">
                        <p>暂停SMTP与POP3服务</p>
                        <br>
                        <el-button type="danger" @click="visible = true;">暂停</el-button>
                    </div>
                </el-col>
                <el-col :span="5">
                    <div class="container">
                        <p>重启SMTP与POP3服务</p>
                        <br>
                        <el-button type="primary" @click="visible = true;">重启</el-button>
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
                        <el-button type="success" @click="visible = true;">启动</el-button>
                    </div>
                </el-col>
                <el-col :span="5">
                    <div class="container">
                        <p>暂停SMTP服务</p>
                        <br>
                        <el-button type="danger" @click="visible = true;">暂停</el-button>
                    </div>
                </el-col>
                <el-col :span="5">
                    <div class="container">
                        <p>重启SMTP服务</p>
                        <br>
                        <el-button type="primary" @click="visible = true;">重启</el-button>
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
                        <el-button type="success" @click="visible = true;">启动</el-button>
                    </div>
                </el-col>
                <el-col :span="5">
                    <div class="container">
                        <p>暂停POP3服务</p>
                        <br>
                        <el-button type="danger" @click="visible = true;">暂停</el-button>
                    </div>
                </el-col>
                <el-col :span="5">
                    <div class="container">
                        <p>重启POP3服务</p>
                        <br>
                        <el-button type="primary" @click="visible = true;">重启</el-button>
                    </div>
                </el-col>
            </el-row>
        </div>
        <el-dialog v-dialogDrag title="拖拽弹框" center :visible.sync="visible" width="30%">
            我是一个可以拖拽的对话框！
            <span slot="footer" class="dialog-footer">
                <el-button @click="visible = false">取 消</el-button>
                <el-button type="primary" @click="visible = false">确 定</el-button>
            </span>
        </el-dialog>
    </section>
</template>

<script>
export default {
    data(){
        return {
            visible: false
        }
    }
}
</script>

<style>

</style>
