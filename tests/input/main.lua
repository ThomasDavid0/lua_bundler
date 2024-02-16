

local sub = require('sub')


function update()
    print('main')
    sub.sub()
    return update, 1000
end

return update()