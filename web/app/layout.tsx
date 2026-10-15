import type {Metadata} from 'next';
import './globals.css';
import './workspace-v4.css';
export const metadata:Metadata={title:'Nhà & Dữ liệu | Giá rao bán TP.HCM',description:'Khám phá dữ liệu tin đăng nhà ở và ước tính giá rao bán bằng Apache Spark. Đồ án Nhập môn Big Data HUIT.'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="vi"><body>{children}</body></html>;}
