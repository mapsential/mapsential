import './LegendItem.css'

export default function LocationInformationItem({name, color}: { name: string, color: string }): JSX.Element {
    return <li className="LegendItem">
        <div className="LegendItem-ColorBox" style={{backgroundColor: color}}></div>
        <span>{name}</span>
    </li>
}