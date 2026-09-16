export type LocalCommand={handled:boolean;intent:'open_app'|'open_url'|'open_folder'|'lock_pc'|'unknown';entity?:string;acknowledgement?:string};
const apps=['chrome','edge','discord','spotify','notepad','calculator','vscode'];
const urls:Record<string,string>={youtube:'https://youtube.com',gmail:'https://gmail.com',google:'https://google.com',shopify:'https://shopify.com'};
export function classifyLocalCommand(input:string):LocalCommand{
 const n=input.toLowerCase().replace(/^(hey|hi|okay|ok)?\s*viper[,.]?\s*/,'').replace(/^(please|can you|could you)\s+/,'').replace(/[.!?]+$/,'').trim();
 const m=n.match(/^(?:open|launch|start|run)(?: up)?\s+(?:my\s+)?(chrome|edge|discord|spotify|notepad|calculator|vscode|vs code)(?:\s+please)?$/);
 if(m){const entity=m[1]==='vs code'?'vscode':m[1];return{handled:true,intent:'open_app',entity,acknowledgement:`Okay boss, I'm opening ${entity==='vscode'?'VS Code':entity} now.`}}
 const u=n.match(/^(?:open|go to|visit)\s+(youtube|gmail|google|shopify)(?:\s+please)?$/);
 if(u)return{handled:true,intent:'open_url',entity:urls[u[1]],acknowledgement:`On it, boss. Opening ${u[1]} now.`};
 const f=n.match(/^(?:open|show|go to)\s+(downloads?|documents?|my downloads|my documents)(?:\s+please)?$/);
 if(f){const entity=f[1].includes('download')?'downloads':'documents';return{handled:true,intent:'open_folder',entity,acknowledgement:`On it, boss. Opening your ${entity} now.`}}
 if(/^(?:lock|lock my|lock the)\s+(?:pc|computer|windows|screen)$/i.test(n)||n==='lock')return{handled:true,intent:'lock_pc',acknowledgement:'Locking the computer now, boss.'};
 return{handled:false,intent:'unknown'}
}
