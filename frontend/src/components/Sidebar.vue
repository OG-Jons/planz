<script setup lang="ts">
import {computed, ref} from 'vue'
import {usePlantsStore} from "@stores/plants.ts";
import logoURL from '../assets/icon_white.svg'
import {useMediaQuery} from "@vueuse/core";

const isExpanded = ref(localStorage.getItem("is_expanded") === "true")

const isLargeScreen = useMediaQuery('(min-width: 1024px)')

const ToggleMenu = () => {
  isExpanded.value = !isExpanded.value
  localStorage.setItem("is_expanded", isExpanded.value.toString())
}

const plantStore = usePlantsStore()

const presets = [
  {
    title: "Home",
    icon: "home",
    to: "/",
  }
]

const menu = computed(() => [
  ...presets,
  ...plantStore.getPlantsWithoutStats.map(plant => ({
    title: plant.name,
    icon: "potted_plant",
    to: `/${plant.id}`,
  }))
])

</script>


<template>
  <aside :class="[{ 'is-expanded': isExpanded }, { 'is-mobile': !isLargeScreen }]">
    <div class="logo">
      <img :src="logoURL" alt="Logo"/>
    </div>

    <!-- Floating toggle for mobile (only when closed) -->
    <div v-if="!isLargeScreen && !isExpanded" class="menu-toggle-float">
      <button class="menu-toggle" @click="ToggleMenu">
        <span class="material-icons">menu</span>
      </button>
    </div>

    <!-- Standard toggle (shown on desktop or when mobile is expanded) -->
    <div v-if="isLargeScreen || isExpanded" class="menu-toggle-wrap">
      <button class="menu-toggle" @click="ToggleMenu">
    <span class="material-icons">
      keyboard_double_arrow_right
    </span>
      </button>
    </div>

    <h3>Menu</h3>
    <div class="menu">
      <router-link v-for="item in menu" :key="item.title" :to="item.to" class="button">
        <span :class="['material-icons', item.to !== '/' ? 'material-symbols-outlined' : '']">{{ item.icon }}</span>
        <span class="text">{{ item.title }}</span>
      </router-link>
    </div>

    <div class="flex"></div>

    <div class="menu">
      <router-link to="/settings" class="button">
        <span class="material-icons">settings</span>
        <span class="text">Settings</span>
      </router-link>
    </div>
  </aside>
</template>


<style lang="scss" scoped>
aside {
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 99;

  background-color: var(--dark);
  color: var(--light);

  width: calc(2rem + 32px);
  overflow: hidden;
  min-height: 100vh;
  padding: 1rem;

  transition: width 0.3s ease-in-out, padding 0.3s ease-in-out;

  .flex {
    flex: 1 1 0;
  }

  .logo {
    margin-bottom: 1rem;

    img {
      width: 2rem;
    }
  }

  .menu-toggle-wrap {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
    position: relative;
    top: 0;
    transition: 0.2s ease-in-out;

    .menu-toggle {
      transition: 0.2s ease-in-out;

      .material-icons {
        font-size: 2rem;
        color: var(--light);
        transition: 0.2s ease-out;
      }
    }
  }

  h3,
  .button .text {
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
  }

  h3 {
    color: var(--grey);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
  }

  .menu {
    margin: 0 -1rem;

    .button {
      display: flex;
      align-items: center;
      text-decoration: none;
      transition: 0.2s ease-in-out;
      padding: 0.5rem 1rem;

      .material-icons {
        font-size: 2rem;
        color: var(--light);
        transition: 0.2s ease-in-out;
      }

      .text {
        color: var(--light);
        transition: 0.2s ease-in-out;
      }

      &.router-link-exact-active {
        background-color: var(--dark-alt);
        border-right: 5px solid var(--primary);

        .material-icons,
        .text {
          color: var(--primary);
        }
      }
    }
  }

  .footer {
    opacity: 0;
    transition: opacity 0.3s ease-in-out;

    p {
      font-size: 0.875rem;
      color: var(--grey);
    }
  }

  &.is-expanded {
    width: var(--sidebar-width);
    padding: 1rem;

    .menu-toggle-wrap {
      top: -3rem;

      .menu-toggle {
        transform: rotate(-180deg);
        transform-origin: center;
      }
    }

    h3,
    .button .text {
      opacity: 1;
    }

    .button .material-icons {
      margin-right: 1rem;
    }

    .footer {
      opacity: 1;
    }
  }

  // Mobile styles
  &.is-mobile {
    width: 0;
    padding: 0;
    overflow: hidden;

    .menu,
    h3,
    .footer {
      display: none;
    }

    .menu-toggle-wrap {
      position: fixed;
      top: 1rem;
      left: 1rem;
      z-index: 1000;
    }

    .menu-toggle {
      background-color: var(--dark);
      border-radius: 50%;
      width: 3rem;
      height: 3rem;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }

    .menu-toggle .material-icons {
      font-size: 2rem;
      color: var(--light);
    }

    &.is-expanded {
      width: var(--sidebar-width);
      padding: 1rem;

      .menu,
      h3,
      .footer {
        display: block;
      }
    }
  }
}

// Hover effects only on devices that support hover
@media (hover: hover) and (pointer: fine) {
  .menu-toggle-wrap .menu-toggle:hover .material-icons {
    color: var(--primary);
    transform: translateX(0.5rem);
  }

  .menu .button:hover {
    background-color: var(--dark-alt);

    .material-icons,
    .text {
      color: var(--primary);
    }
  }
}

.menu-toggle-float {
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 1000;

  .menu-toggle {
    background-color: var(--dark);
    border-radius: 50%;
    width: 3rem;
    height: 3rem;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);

    .material-icons {
      font-size: 2rem;
      color: var(--light);
    }
  }
}
</style>