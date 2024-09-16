<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">

      <nav>
        <div class="navbar">
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/about">About</RouterLink>
          <RouterLink to="/sources">Sources</RouterLink>
        </div>
      </nav>
    </div>
  </header>

  <RouterView class="router-view"/>
</template>

<style>
  .navbar {
    position:fixed;
    background-color: var(--dark-color);
    display: flex;
    flex-direction: row;
    column-gap: 1em;
    padding: 0.5em;
    font-size: 1.2em;
    font-family: "Roboto Condensed", sans-serif;
    font-weight: 500;
    width: 100%;
    a {
      color: var(--light-color);
      text-decoration: none;
    }
    a:hover {
      color: var(--accent-color);
    }
  }
</style>
