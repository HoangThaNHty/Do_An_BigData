import * as React from 'react';
import {Slot} from '@radix-ui/react-slot';
import {cva,type VariantProps} from 'class-variance-authority';
import {cn} from '@/lib/utils';
const variants=cva('inline-flex items-center justify-center gap-2 rounded-lg text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-700 disabled:pointer-events-none disabled:opacity-50',{
  variants:{variant:{default:'bg-teal-800 text-white hover:bg-teal-900',outline:'border border-stone-300 bg-white hover:bg-stone-100',ghost:'hover:bg-stone-100'},size:{default:'h-10 px-4',sm:'h-9 px-3',icon:'size-10'}},defaultVariants:{variant:'default',size:'default'}
});
export function Button({className,variant,size,asChild=false,...props}:React.ComponentProps<'button'>&VariantProps<typeof variants>&{asChild?:boolean}){
  const Comp=asChild?Slot:'button';return <Comp className={cn(variants({variant,size,className}))} {...props}/>;
}
