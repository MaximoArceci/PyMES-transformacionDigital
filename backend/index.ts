import { Elysia } from "elysia";
import {router } from "./endpoints";

const app = new Elysia();

app.use(router).listen(3000);