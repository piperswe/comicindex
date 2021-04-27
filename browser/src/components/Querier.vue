<template>
  <div class="querier">
    <b-button variant="danger" v-on:click="resetQuery">reset query</b-button>
    <prism-editor
      class="query"
      v-model="query"
      :highlight="highlighter"
      line-numbers></prism-editor>

    <b-table-simple class="table" v-if="result">
      <b-thead>
      <b-tr>
        <b-th scope="col"
            v-for="column in result.columns"
            v-bind:key="JSON.stringify({ column })">
          {{ column }}
        </b-th>
      </b-tr>
      </b-thead>
      <b-tbody>
      <b-tr v-for="(row, rowIndex) in result.values" v-bind:key="rowIndex">
        <b-td v-for="(value, valueIndex) in row" v-bind:key="`${rowIndex}-${valueIndex}`">
          <a v-if="isURL(value)" v-bind:href="value">{{ value }}</a>
          <a v-else-if="isPhoneNumber(value)" v-bind:href="'tel:' + value">{{ value }}</a>
          <a v-else-if="isEmail(value)" v-bind:href="'mailto:' + value">{{ value }}</a>
          <a v-else-if="isOSM(value)" v-bind:href="osmLink(value)">{{ value }}</a>
          <span v-else>{{ value }}</span>
        </b-td>
      </b-tr>
      </b-tbody>
    </b-table-simple>
  </div>
</template>

<style scoped>
.querier {
  width: 100%;
  display: flex;
  flex-direction: column;
}
.query {
  width: 100%;

  color: #ccc;
  background: none;
  font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
  font-size: 1em;
  text-align: left;
  white-space: pre;
  word-spacing: normal;
  word-break: normal;
  word-wrap: normal;
  line-height: 1.5;

  -moz-tab-size: 4;
  -o-tab-size: 4;
  tab-size: 4;

  -webkit-hyphens: none;
  -moz-hyphens: none;
  -ms-hyphens: none;
  hyphens: none;

  padding: 1em;
  margin: .5em 0;
  overflow: auto;
}
.table {
  --margin: 20px;
  width: calc(100% - 2 * var(--margin));
  margin: var(--margin);
  display: block;
  overflow-x: scroll;
}
td {
  min-width: 100px;
}
</style>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Database, QueryExecResult, SqlValue } from 'sql.js';
import { PrismEditor } from 'vue-prism-editor';
import 'vue-prism-editor/dist/prismeditor.min.css';
import { highlight, languages } from 'prismjs';
import 'prismjs/components/prism-sql';
import 'prismjs/themes/prism-tomorrow.css';

function isString(x: SqlValue): x is string {
  return typeof x === 'string';
}

@Component({
  components: {
    PrismEditor,
  },
})
export default class Querier extends Vue {
  private queryValue = '';

  private defaultQueryValue: Promise<string> | null = null;

  @Prop() private db!: Database;

  get query(): string {
    return this.queryValue;
  }

  set query(q: string) {
    localStorage.setItem('query', q);
    this.queryValue = q;
  }

  get defaultQuery(): Promise<string> {
    if (this.defaultQueryValue == null) {
      // eslint-disable-next-line global-require,@typescript-eslint/no-var-requires
      this.defaultQueryValue = fetch(require('../assets/default.sql')).then((res) => res.text());
    }
    return this.defaultQueryValue;
  }

  async created(): Promise<void> {
    // eslint-disable-next-line global-require,@typescript-eslint/no-var-requires
    this.query = localStorage.getItem('query') || await this.defaultQuery;
  }

  async resetQuery(): Promise<void> {
    this.query = await this.defaultQuery;
  }

  get result(): QueryExecResult | null {
    console.log('Querying:', this.query);
    try {
      return this.db ? this.db.exec(this.query)[0] : null;
    } catch (e) {
      console.warn(e);
      return null;
    }
  }

  isURL(x: SqlValue): x is string {
    if (!isString(x)) return false;
    const re = /(?![^<]*>|[^<>]*<\/)((https?:)\/\/[a-z0-9&#=./\-?_]+)/gi;
    return re.test(x);
  }

  isPhoneNumber(x: SqlValue): x is string {
    if (!isString(x)) return false;
    const re = /^\+?[\s\-\d()]{10,}$/;
    return re.test(x);
  }

  isEmail(x: SqlValue): x is string {
    if (!isString(x)) return false;
    const re = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
    return re.test(x);
  }

  isOSM(x: SqlValue): x is string {
    if (!isString(x)) return false;
    const re = /^[NWR]\d+$/;
    return re.test(x);
  }

  osmLink(x: SqlValue): string {
    if (!isString(x)) return '';
    const chToPath: { [ch: string]: string } = {
      N: 'node',
      W: 'way',
      R: 'relation',
    };
    return `https://openstreetmap.org/${chToPath[x.substring(0, 1)]}/${x.substring(1)}`;
  }

  highlighter(code: string): string {
    return highlight(code, languages.sql, 'sql');
  }
}
</script>
