import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    inputStr: "",
    value: "1",
    name:"",
    hasSearched:[],
    entityNode: [],
    entityLinks: [],
    porpertyNode:[],
    porpertyLinks:[],
    typeNode:[],
    typeLinks:[],
    typeMap:{},
    newstop:[],
    img:"",
    abstract:"",
    newsImg:[],
    statu:true,
    explore:false,
    key_word_id:0,
    path:"实体图",
    first:false,
  },
  mutations: {
    changeInputStr(state,item){
      state.inputStr=item
    },
    changeValue(state,item){
      state.value=item
    },
    changeName(state,item){
      state.name=item
    },
    changeSearched(state,item){
      state.hasSearched=item
    },
    changeEntityNode(state,item){
      state.entityNode=item
    },
    changeEntityLinks(state,item){
      state.entityLinks=item
    },
    changeTypeLinks(state,item){
      state.typeLinks=item
    },
    changeTypeNode(state,item){
      state.typeNode=item
    },
    changeTypeMap(state,item){
      state.typeMap=item
    },
    changePorpertyLinks(state,item){
      state.porpertyLinks=item
    },
    changePorpertyNode(state,item){
      state.porpertyNode=item
    },
    changeNewsTop(state,item){
      state.newstop=item
    },
    changeImg(state,item){
      state.img=item
    },
    changeAbstract(state,item){
      state.abstract=item
    },
    changeNewsimg(state,item){
      state.newsImg=item
    },
    changeStatu(state,item){
      state.statu=item
    },
    changeExplore(state,item){
      state.explore=item
    },
    changeKey_word_id(state,item){
      state.key_word_id=item
    },
    changePath(state,item){
      state.path=item
    },
    changeFirst(state,item){
      state.first=item
    },
  },
  actions: {
  },
  modules: {
  }
})
