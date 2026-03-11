import Dexie from "dexie";

export const db = new Dexie("chatDB");

db.version(1).stores({
  chats: "++id"
});