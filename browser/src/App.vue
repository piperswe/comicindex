<template>
  <div id="app">
    <div class="container">
      <h1>comicindex data explorer</h1>
      <p>query automatically runs as you type</p>
    </div>
    <Querier v-bind:db="db" />
    <div class="container">
      <h2>Licenses</h2>
      <ul>
        <li v-for="license in licenses" v-bind:key="license">{{ license }}</li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import initSqlJs, { Database, SqlValue } from 'sql.js';
import Querier from './components/Querier.vue';

declare global {
  interface Window {
    db: Database,
  }
}

@Component({
  components: {
    Querier,
  },
})
export default class App extends Vue {
  db: Database | null = null;

  get licenses(): SqlValue[] | null {
    return this.db ? this.db.exec('SELECT license FROM licenses')[0].values.map((x) => x[0]) : null;
  }

  async created(): Promise<void> {
    const sqlPromise = initSqlJs({
      locateFile: (file) => `https://sql.js.org/dist/${file}`,
    });
    const dataPromise = fetch('https://piperswe.github.io/comicindex/comic.index').then((res) => res.arrayBuffer());
    const [SQL, buf] = await Promise.all([
      sqlPromise,
      dataPromise,
    ]);
    const db = new SQL.Database(new Uint8Array(buf));
    window.db = db;
    this.db = db;
  }
}
</script>

<style>
#app {
}
</style>
