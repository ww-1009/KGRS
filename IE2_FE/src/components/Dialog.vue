<template>
  <div>
    <el-dialog
      title="实体关系"
      :visible.sync="dialog_child"
      width="30%"
      top="30vh"
			append-to-body
    >
      <span>这是一段信息</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialog_child = false">取 消</el-button>
        <!-- <el-button type="primary" @click="dialogYes">确 定</el-button> -->
      </span>
    </el-dialog>
  </div>
</template>
<script>
export default {
  components: { Myimage, Mysearch },
  data() {
    return {
      dialog_child: false,
    };
  },
};
</script>