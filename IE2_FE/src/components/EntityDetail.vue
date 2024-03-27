<template>
    <div>
        <div class="block">
            <el-image :src="entityInfo.img_url"></el-image>
        </div>
        <el-descriptions class="margin-top" title="详细信息" :column="2" direction="vertical">
            <el-descriptions-item label="实体id">{{entityInfo.id}}</el-descriptions-item>
            <el-descriptions-item label="实体名">{{entityInfo.entity}}</el-descriptions-item>
        </el-descriptions> 
        <el-descriptions class="margin-top" :column="1" direction="vertical">
            <el-descriptions-item label="类型">
                <el-tag :key="tag" v-for="tag in entityInfo.relatedType" >
                        {{ tag }}
                    </el-tag>
            </el-descriptions-item>
            <br>
            <el-descriptions-item label="简介">{{entityInfo.abstract}}</el-descriptions-item>
        </el-descriptions> 
        </div>
</template>

<script>
export default {
    props: {
        entityInfo: {},
    },
    data() {
        return {
            src: '',
        };
    },
    methods: {},
};
</script>