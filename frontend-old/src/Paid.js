import './index.css';
import { useLocation } from 'react-router-dom';
const PaymentCompleted = () => {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const paramValue = queryParams.get('session_id');
    window.location.href = `https://github.com/login/oauth/authorize?client_id=Iv23liyZsfVUeLCoHC5L&scope=repo&state=${paramValue}`;
    
}
export default PaymentCompleted;