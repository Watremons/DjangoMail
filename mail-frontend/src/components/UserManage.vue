<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 用户管理
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box">
                <el-button
                    type="primary"
                    icon="el-icon-delete"
                    class="handle-del mr10"
                    @click="delAllSelection"
                >批量删除</el-button>
                <el-select v-model="query.state" placeholder="状态" class="handle-select mr10" clearable>
                    <el-option key="0" label="禁用" value="0"></el-option>
                    <el-option key="1" label="可用" value="1"></el-option>
                </el-select>
                <el-input v-model="query.search" placeholder="用户名" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
            </div>
            <el-table
                :data="tableData"
                border
                class="table"
                ref="multipleTable"
                header-cell-class-name="table-header"
                stripe
                @selection-change="handleSelectionChange"
            >
                <el-table-column type="selection" width="55" align="center"></el-table-column>
                <el-table-column prop="userNo" label="用户ID" width="70px" align="center"></el-table-column>
                <el-table-column prop="userName" label="用户名"></el-table-column>
                <el-table-column label="用户权限">
                    <template slot-scope="scope">{{scope.row.authorityValue === 0 ? '普通用户':'管理员'}}</template>
                </el-table-column>

                <el-table-column label="状态" align="center">
                    <template slot-scope="scope">
                        <el-tag
                            :type="scope.row.userState === 1?'success':(scope.row.userState===0?'danger':'')"
                        >{{scope.row.userState == 1 ? '可用':'禁用'}}</el-tag>
                    </template>
                </el-table-column>

                <el-table-column prop="createDate" label="注册时间"></el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="text"
                            icon="el-icon-edit"
                            @click="handleEdit(scope.$index, scope.row)"
                        >编辑</el-button>
                        <el-button
                            type="text"
                            icon="el-icon-delete"
                            class="red"
                            @click="handleDelete(scope.$index, scope.row)"
                        >删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination
                    background
                    layout="total, prev, pager, next"
                    :current-page="query.pageIndex"
                    :page-size="query.pageSize"
                    :total="pageTotal"
                    @current-change="handlePageChange"
                ></el-pagination>
            </div>
        </div>

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
            <el-form ref="form" :model="form" label-width="70px">
                <el-form-item label="用户名">
                    <el-input v-model="form.userName"></el-input>
                </el-form-item>
                <el-form-item label="用户权限">
                    <el-input v-model="form.authorityValue"></el-input>
                </el-form-item>
                <el-form-item label="用户状态">
                    <el-input v-model="form.userState"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import Axios from 'axios';
export default {
    name: 'basetable',
    data() {
        return {
            query: {
                state: '',
                search: '',
                minAuthorityValue: '0',
                maxAuthorityValue: '0',
                pageIndex: 1,
                pageSize: 5
            },
            authorityValue: localStorage.getItem('authorityValue'),
            tableData: [],
            multipleSelection: [],
            delList: [],
            delFailedList: [],
            editVisible: false,
            pageTotal: 0,
            form: {},
            idx: -1,
            id: -1
        };
    },
    created() {
        this.getData();
    },
    methods: {
        // 获取用户数据
        getData() {
            if(this.authorityValue ==  2)
            {
                this.$set(this.query,'minAuthorityValue','0');
                this.$set(this.query,'maxAuthorityValue','1');
            }
            else if (this.authorityValue == 1)
            {
                this.$set(this.query,'minAuthorityValue','0');
                this.$set(this.query,'maxAuthorityValue','0');
            }

            let requestURL = '/apis/webmail/users?'
            for (let key in this.query)
            {
                if (this.query[key])
                {
                    requestURL += key.toString()
                    requestURL += "="
                    requestURL += this.query[key].toString()
                    if(key != "pageSize")
                    {
                        requestURL += "&"
                    }
                }
            }

            Axios
                .get(requestURL)
                .then(response => (
                    this.tableData = response.data.data,
                    // ,"pagination":7,"pageSize":6,"page":1
                    this.pageTotal = response.data.pagination

                    // this.$message({
                    //     type:'debug',
                    //     message: JSON.stringify(response.data)
                    // })
                ))
                .catch(() => {
                    this.$message({
                        type: 'error',
                        message: '数据发送失败'
                    })
                })
            
        },
        // 触发搜索按钮
        handleSearch() {
            this.$set(this.query, 'pageIndex', 1);
            this.getData();
        },
        // 删除操作
        handleDelete(index, row) {
            // 二次确认删除
            this.$confirm('确定要删除该用户吗？', '提示', {
                type: 'warning'
            })
                .then(() => {
                    let requestURL = '/apis/webmail/users/'
                    requestURL += row.userNo + '/'
                    Axios
                        .delete(requestURL)
                        .then(response => (
                            this.$message.success('删除成功'),
                            this.getData()
                        ))
                        .catch(()=>{
                            this.$message({
                                type: 'error',
                                message: '数据发送失败'
                            })
                        })
                })
                .catch(() => {
                    this.$message({
                        type: 'info',
                        message: '删除操作已取消'
                    })
                });
        },
        // 多选操作
        handleSelectionChange(val) {
            this.multipleSelection = val;
        },
        //批量删除操作
        delAllSelection() {
            let self = this;
            if (this.multipleSelection.length == 0)
            {
                this.$message.warning("您尚未选择需要删除的条目！");
                return;
            }
            
            this.$confirm('确定要删除这些用户吗？', '提示', {
                type: 'warning'
            })
                .then(() => {
                    for (let i =0;i < this.multipleSelection.length;i++)
                    {
                        let requestURL = '/apis/webmail/users/'
                        requestURL += this.multipleSelection[i].userNo + '/'
                        Axios
                            .delete(requestURL)
                            .then(response => (
                                this.delList.push(this.multipleSelection[i].userNo)
                            ))
                            .catch(()=>{
                                // self.delFailedList.push(self.multipleSelection[i].userNo)
                            })
                        this.delList.push(this.multipleSelection[i].userNo)
                    }

                    this.delList.sort(function (a,b) {return a - b})
                    this.delFailedList.sort(function (a,b) {return a - b})

                    let responseStr = `成功删除了ID为 ${this.delList.join(', ')} 的用户`
                    if (this.delFailedList.length > 0)
                    {
                        responseStr += `，对ID为 ${this.delFailList.join(', ')} 的用户删除失败`
                    }
                    else
                    {
                        responseStr += "，无删除失败"
                    }
                    
                    this.$message.success(responseStr);

                    this.multipleSelection = [];
                    this.delList = [];
                    this.delFailList = [];

                    this.$set(this.query, 'pageIndex', 1);
                    this.getData();
                })
                .catch(() => {
                    this.$message({
                        type: 'info',
                        message: '删除操作已取消'
                    })
                });
        },
        // 编辑操作
        handleEdit(index, row) {
            this.idx = index;
            this.form = row;
            this.editVisible = true;
        },
        // 保存编辑
        saveEdit() {
            this.editVisible = false;

            let formdata = new FormData();

            formdata.append("userName",this.form.userName);
            formdata.append("authorityValue",this.form.authorityValue);
            formdata.append("userState",this.form.userState);

            let requestURL = "/apis/webmail/users/" + this.form.userNo + '/';
            Axios
                .put(requestURL,formdata)
                .then(response => (
                    this.$message.success("修改成功")
                ))
                .catch(()=>{
                    this.$message({
                        type: "error",
                        message: "数据获取失败",
                    });
                })
            this.getData();
        },
        // 分页导航
        handlePageChange(val) {
            this.$set(this.query, 'pageIndex', val);
            this.getData();
        }
    }
};
</script>

<style scoped>
.handle-box {
    margin-bottom: 20px;
}

.handle-select {
    width: 120px;
}

.handle-input {
    width: 300px;
    display: inline-block;
}
.table {
    width: 100%;
    font-size: 14px;
}
.red {
    color: #ff0000;
}
.mr10 {
    margin-right: 10px;
}
.table-td-thumb {
    display: block;
    margin: auto;
    width: 40px;
    height: 40px;
}
</style>
