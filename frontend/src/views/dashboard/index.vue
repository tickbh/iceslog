<template>
  <div class="dashboard-container">
    <!-- github角标 -->
    <github-corner class="github-corner" />

    <!-- <el-card shadow="never">
      <el-row justify="space-between">
        <el-col :span="18" :xs="24">
          <div class="flex h-full items-center">
            <img
              class="w-20 h-20 mr-5 rounded-full"
              :src="userStore.user.avatar + '?imageView2/1/w/80/h/80'"
            />
            <div>
              <p>{{ greetings }}</p>
              <p class="text-sm text-gray">
                今日天气晴朗，气温在15℃至25℃之间，东南风。
              </p>
            </div>
          </div>
        </el-col>

        <el-col :span="6" :xs="24">
          <div class="flex h-full items-center justify-around">
            <el-statistic
              v-for="item in statisticData"
              :key="item.key"
              :value="item.value"
            >
              <template #title>
                <div class="flex items-center">
                  <svg-icon :icon-class="item.iconClass" size="20px" />
                  <span class="text-[16px] ml-1">{{ item.title }}</span>
                </div>
              </template>
              <template v-if="item.suffix" #suffix>/100</template>
            </el-statistic>
          </div>
        </el-col>
      </el-row>
    </el-card> -->

    <el-button icon="el-icon-arrow-left" class="pan-back-btn" @click="do_log">
      小量日志
    </el-button>

    <el-button icon="el-icon-arrow-left" class="pan-back-btn" @click="do_logs">
      大量日志
    </el-button>

    <!-- 数据卡片 -->
    <!-- <el-row :gutter="10" class="mt-5">
      <el-col
        :xs="24"
        :sm="12"
        :lg="6"
        v-for="(item, index) in cardData"
        :key="index"
      >
        <el-card shadow="never">
          <template #header>
            <div class="flex items-center justify-between">
              <span class="text-[var(--el-text-color-secondary)]">{{
                item.title
              }}</span>
              <el-tag v-if="item.tagText" :type="item.tagType" size="small">
                {{ item.tagText }}
              </el-tag>
            </div>
          </template>

          <div class="flex items-center justify-between mt-2">
            <div class="text-lg text-right">
              {{ Math.round(item.count) }}
            </div>
            <svg-icon :icon-class="item.iconClass" size="2em" />
          </div>

          <div
            class="flex items-center justify-between mt-2 text-sm text-[var(--el-text-color-secondary)]"
          >
            <span> {{ item.dataDesc }} </span>
            <span> {{ item.totalCount }} </span>
          </div>
        </el-card>
      </el-col>
    </el-row> -->

    <!-- Echarts 图表 -->
    <el-row :gutter="10" class="mt-5">
      <el-col :xs="24" :span="24">
        <VisitTrend id="VisitTrend" width="100%" height="400px" />
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import type { EpPropMergeType } from "element-plus/es/utils/vue/props/types";
defineOptions({
  name: "Dashboard",
  inheritAttrs: false,
});

import { useUserStore } from "@/store/modules/user";
import { useTransition, TransitionPresets } from "@vueuse/core";
import ApiLogAPI from "@/api/api_log";
function guid() {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
    var r = (Math.random() * 16) | 0,
      v = c == "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

function do_log() {
  ApiLogAPI.add_one({
    create: new Date(),
    lv: 2,
    tid: guid(),
    uid: 1,
    sys: "Web",
    msg: "测试日志111111111xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbb",
    exid: "222222222222",
    extra:
      "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbfffffffffffffffffffffffffffffffeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeerwqrewrwerwerew",
  });
}

function do_logs() {
  var many = [];
  for (let index = 0; index < 5; index++) {
    many.push({
      create: new Date(),
      lv: 1,
      tid: guid(),
      uid: 1,
      sys: index % 2 == 1 ? "IOS" : "Android",
      msg:
        index % 2 == 1
          ? "测试日志111111111xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbb"
          : "我是测试内容ccc",
      exid: "222222222222",
      extra:
        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbfffffffffffffffffffffffffffffffeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeerwqrewrwerwerew",
    });
  }
  ApiLogAPI.add_many(many);
}

const userStore = useUserStore();
const date: Date = new Date();

const greetings = computed(() => {
  const hours = date.getHours();
  if (hours >= 6 && hours < 8) {
    return "晨起披衣出草堂，轩窗已自喜微凉🌅！";
  } else if (hours >= 8 && hours < 12) {
    return "上午好，" + userStore.user.nickname + "！";
  } else if (hours >= 12 && hours < 18) {
    return "下午好，" + userStore.user.nickname + "！";
  } else if (hours >= 18 && hours < 24) {
    return "晚上好，" + userStore.user.nickname + "！";
  } else {
    return "偷偷向银河要了一把碎星，只等你闭上眼睛撒入你的梦中，晚安🌛！";
  }
});

const duration = 5000;

// 在线用户数
const onlineUserCount = ref(0);
const onlineUserCountOutput = useTransition(onlineUserCount, {
  duration: duration,
  transition: TransitionPresets.easeOutExpo,
});
onlineUserCount.value = 1;

// 浏览量
const pvCount = ref(0);
const pvCountOutput = useTransition(pvCount, {
  duration: duration,
  transition: TransitionPresets.easeOutExpo,
});
pvCount.value = 2000;

// 访客数
const uvCount = ref(0);
const uvCountOutput = useTransition(uvCount, {
  duration: duration,
  transition: TransitionPresets.easeOutExpo,
});
uvCount.value = 2000;

// IP数
const ipCount = ref(0);
const ipCountOutput = useTransition(ipCount, {
  duration: duration,
  transition: TransitionPresets.easeOutExpo,
});
ipCount.value = 2000;

// 右上角数量
const statisticData = ref([
  {
    value: 99,
    iconClass: "message",
    title: "消息",
    key: "message",
  },
  {
    value: 50,
    iconClass: "todolist",
    title: "待办",
    suffix: "/100",
    key: "upcoming",
  },
  {
    value: 10,
    iconClass: "project",
    title: "项目",
    key: "project",
  },
]);

interface CardProp {
  title: string;
  tagType: EpPropMergeType<
    StringConstructor,
    "primary" | "success" | "info" | "warning" | "danger",
    unknown
  >;
  tagText: string;
  count: any;
  totalCount: any;
  dataDesc: string;
  iconClass: string;
}
// 卡片数量
const cardData = ref<CardProp[]>([
  {
    title: "在线用户",
    tagType: "success",
    tagText: "-",
    count: onlineUserCountOutput,
    totalCount: "3",
    dataDesc: "总用户数",
    iconClass: "visit",
  },
  {
    title: "浏览量(PV)",
    tagType: "primary",
    tagText: "日",
    count: pvCountOutput,
    totalCount: 3000,
    dataDesc: "总浏览量",
    iconClass: "pv",
  },
  {
    title: "访客数(UV)",
    tagType: "danger",
    tagText: "日",
    count: uvCountOutput,
    totalCount: 3000,
    dataDesc: "总访客数",
    iconClass: "uv",
  },
  {
    title: "IP数",
    tagType: "success",
    tagText: "日",
    count: ipCountOutput,
    totalCount: 3000,
    dataDesc: "总IP数",
    iconClass: "ip",
  },
]);

// 通知公告数据
const notices = ref([
  {
    title: "系统更新",
    content: "系统将于今晚22:00进行更新，请提前保存好工作。",
  },
  {
    title: "假期通知",
    content: "国庆假期将于10月1日开始，请提前做好工作安排。",
  },
  {
    title: "紧急通知",
    content: "请所有员工注意，明天将进行紧急疏散演练。",
  },
]);
</script>

<style lang="scss" scoped>
.dashboard-container {
  position: relative;
  padding: 24px;

  .user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }

  .github-corner {
    position: absolute;
    top: 0;
    right: 0;
    z-index: 1;
    border: 0;
  }

  .data-box {
    display: flex;
    justify-content: space-between;
    padding: 20px;
    font-weight: bold;
    color: var(--el-text-color-regular);
    background: var(--el-bg-color-overlay);
    border-color: var(--el-border-color);
    box-shadow: var(--el-box-shadow-dark);
  }

  .svg-icon {
    fill: currentcolor !important;
  }
}
</style>
