import React from 'react'
import { Select } from 'antd';
const { Option } = Select;

function SearchableSelect({options, onChange, placeholder}) {
  return (
    <Select
      showSearch
      placeholder={placeholder}
      optionFilterProp="children"
      onChange={onChange}
      filterOption={(input, option) =>
        option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
      }
      style={{width: "100%"}}

    >
      {options.map((option, ix) => {
        return <Option value = {option} key = {ix}>
          {option}
        </Option>
      })}
    </Select>
  )
}

export default SearchableSelect;
