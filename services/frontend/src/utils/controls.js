import AdjustAnimation from "@/components/controls/AdjustAnimation.vue";
import ChangeBackground from "@/components/controls/ChangeBackground.vue";
import CompositionSettings from "@/components/controls/CompositionSettings.vue";
import DeleteAnimation from "@/components/controls/DeleteAnimation.vue";
import GoHome from "@/components/controls/GoHome.vue";
import RecordAnimation from "@/components/controls/RecordAnimation.vue";
import RefreshAnimation from "@/components/controls/RefreshAnimation.vue";
import RenameAnimation from "@/components/controls/RenameAnimation.vue";
import SetUpSpeed from "@/components/controls/SetUpSpeed.vue";

export const leftControls = [
  { title: "Переименовать", component: RenameAnimation },
  { title: "Выбор анимации", component: AdjustAnimation },
  { title: "Ускорить/Замедлить", component: SetUpSpeed },
  { title: "Изменить фон", component: ChangeBackground },
  {
    title: "Композиция",
    component: CompositionSettings,
  },
];

export const rightControls = [
  { title: "Обновить", component: RefreshAnimation },
  { title: "Записать видео", component: RecordAnimation },
  { title: "Удалить", component: DeleteAnimation },
  { title: "Вернуться домой", component: GoHome },
];
