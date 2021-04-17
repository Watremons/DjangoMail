<template>
    <section class="main">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-global"></i> {{helpMessages.breadcrumb}}</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <span>{{helpMessages.tips}}</span>
            <!-- <el-button type="primary">{{helpMessages.btn}}</el-button> -->
            <div class="list">
            <h2>{{helpMessages.title1}}</h2>
                <p>{{helpMessages.p1content1}}</p>
                <p>{{helpMessages.p1content2}}</p>
                <p>{{helpMessages.p1content3}}</p>
            </div>
            <div class="list">
            <h2>{{helpMessages.title2}}</h2>
                <p>{{helpMessages.p2content1}}</p>
                <p>{{helpMessages.p2content2}}</p>
            </div>
            <div class="list">
            <h2>{{helpMessages.title3}}</h2>
                <p>{{helpMessages.p3content1}}</p>
                <p>{{helpMessages.p3content2}}</p>
                <p>{{helpMessages.p3content3}}</p>
            </div>
            <div class="list">
            <h2>{{helpMessages.title4}}</h2>
                <p>{{helpMessages.p4content1}}</p>
                <p>{{helpMessages.p4content2}}</p>
                <p>{{helpMessages.p4content3}}</p>
            </div>
        </div>
    </section>
</template>

<script>
import {
    helpMessages 
}from './common/help';

export default {
    data(){
        return {
            helpMessages
        }
    }
}
</script>

<style scoped>
.list{
    padding: 30px 0;
}
.list p{
    margin-bottom: 20px;
}
a{
    color: #409eff;
}
</style>
